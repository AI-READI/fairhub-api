"""APIs for study operations""" ""
import os
import re
from typing import Any, Union

import requests
from azure.storage.filedatalake import FileSystemClient
from flask import Response, g, request
from flask_restx import Namespace, Resource, fields, reqparse
from jsonschema import ValidationError, validate

import config
import model

from .authentication import is_granted

api = Namespace("Study", description="Study operations", path="/")


study_model = api.model(
    "Study",
    {
        "title": fields.String(required=True, default=""),
    },
)


@api.route("/study")
class Studies(Resource):
    """All studies"""

    parser_study = reqparse.RequestParser(bundle_errors=True)
    parser_study.add_argument(
        "title", type=str, required=True, location="json", help="The title of the Study"
    )
    parser_study.add_argument(
        "image",
        type=list,
        required=True,
        location="json",
        help="The image for the Study",
    )

    @api.doc(description="Return a list of all studies")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(study_model)
    def get(self):
        """Return a list of all studies"""
        study_contributors = model.StudyContributor.query.filter(
            model.StudyContributor.user_id == g.user.id
        ).all()  # Filter contributors where user_id matches the user's id

        study_ids = [contributor.study_id for contributor in study_contributors]

        studies = model.Study.query.filter(model.Study.id.in_(study_ids)).all()

        return [s.to_dict() for s in studies], 200

    # @api.expect(study_model)
    @api.response(201, "Success")
    @api.response(400, "Validation Error")
    def post(self):
        """Create a new study"""

        # Schema validation
        schema = {
            "type": "object",
            "required": ["title", "image", "short_description"],
            "additionalProperties": False,
            "properties": {
                "title": {"type": "string", "minLength": 1, "maxLength": 300},
                "short_description": {"type": "string", "maxLength": 300},
                "image": {"type": "string"},
                "clinical_id": {"type": ["string", "null"]},
            },
        }

        data: Union[Any, dict] = request.json
        add_study = model.Study.from_data(data)
        identifier = data.get("clinical_id")

        try:
            validate(instance=data, schema=schema)
        except ValidationError as e:
            return e.message, 400

        model.db.session.add(add_study)

        study_id = add_study.id
        study_ = model.Study.query.get(study_id)

        study_contributor = model.StudyContributor.from_data(study_, g.user, "owner")
        model.db.session.add(study_contributor)

        if os.environ.get("FLASK_ENV") != "testing":
            # TODO finish study testing integration
            container = config.AZURE_CONTAINER
            if config.AZURE_STORAGE_CONNECTION_STRING and config.AZURE_CONTAINER:
                file_system_client = FileSystemClient.from_connection_string(
                    config.AZURE_STORAGE_CONNECTION_STRING,
                    file_system_name=container,
                )
                file_system_client.create_directory(f"AI-READI/test-files/{study_id}")
            try:
                if isinstance(identifier, str) and re.match(r"^NCT\d{8}$", identifier.strip()):

                    url = f"https://classic.clinicaltrials.gov/api/v2/studies/{identifier}"
                    # AI-READI id-NCT06002048

                    response = requests.get(url, timeout=10)
                    if response.status_code == 404:
                        return {
                            "error": "No clinical study was found with the provided identifier",
                            "status_code": 404,
                            "message": f"No study found for identifier '{identifier}'."
                        }, 404

                    if response.status_code != 200:
                        return {
                            "error": "Failed to fetch clinical trial data",
                            "status_code": response.status_code,
                            "message": f"ClinicalTrials.gov returned status {response.status_code}."
                        }, response.status_code

                    clinical_data = response.json()
                    study_.update_identification_id(clinical_data["protocolSection"])
                    study_.import_from_clinical_data(
                        clinical_data["protocolSection"]
                    )
            except requests.exceptions.RequestException as e:
                return {
                    "error": "Failed to connect to ClinicalTrials.gov API",
                    "status_code": 503,
                    "message": str(e)
                }, 503
            except Exception as e:
                return {
                    "error": "Unexpected server error",
                    "status_code": 500,
                    "message": str(e)
                }, 500
        model.db.session.commit()

        return study_.to_dict(), 201


@api.route("/study/<study_id>")
class StudyResource(Resource):
    """Return a study's details"""

    @api.doc(description="Get a study's details")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(study)
    def get(self, study_id: int):
        """Return a study's details"""
        study1 = model.Study.query.get(study_id)

        return study1.to_dict(), 200

    @api.expect(study_model)
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.doc(description="Update a study's details")
    def put(self, study_id: int):
        """Update a study"""
        # Schema validation
        schema = {
            "type": "object",
            "required": ["title", "short_description", "is_overwrite"],
            "additionalProperties": False,
            "properties": {
                "title": {"type": "string", "minLength": 1},
                "short_description": {"type": "string", "maxLength": 300},
                "is_overwrite": {"type": "boolean"},
                "clinical_id": {"type": ["string", "null"]},
            },
        }

        try:
            validate(request.json, schema)
        except ValidationError as e:
            return e.message, 400

        update_study = model.Study.query.get(study_id)
        data: Union[Any, dict] = request.json
        if not is_granted("update_study", update_study):
            return "Access denied, you can not modify", 403

        identifier = data["clinical_id"].strip()
        is_overwrite = data["is_overwrite"]

        update_study.update(data)

        if identifier:
            try:
                if not identifier or not isinstance(identifier, str):
                    raise ValueError("Identifier must be a non-empty string.")

                if not re.match(r"^NCT\d{8}$", identifier):
                    raise ValueError("Identifier must be in the format 'NCT########'.")

                url = f"https://classic.clinicaltrials.gov/api/v2/studies/{identifier}"

                response = requests.get(url, timeout=10)
                if response.status_code == 404:
                    return {
                        "error": "No clinical study was found with the provided identifier",
                        "status_code": 404,
                        "message": f"No study found for identifier '{identifier}'."
                    }, 404

                if response.status_code != 200:
                    return {
                        "error": "Failed to fetch clinical trial data",
                        "status_code": response.status_code,
                        "message": f"ClinicalTrials.gov returned status {response.status_code}."
                    }, response.status_code

                clinical_data = response.json()
                update_study.update_identification_id(clinical_data["protocolSection"])
                if is_overwrite:
                    update_study.import_from_clinical_data(
                        clinical_data["protocolSection"]
                    )
            except requests.exceptions.RequestException as e:
                return {
                    "error": "Failed to connect to ClinicalTrials.gov API",
                    "status_code": 503,
                    "message": str(e)
                }, 503
            except Exception as e:
                return {
                    "error": "Unexpected server error",
                    "status_code": 500,
                    "message": str(e)
                }, 500

        model.db.session.commit()

        return update_study.to_dict(), 200

    @api.response(204, "Success")
    @api.response(400, "Validation Error")
    @api.doc(description="Delete a study")
    def delete(self, study_id: int):
        """Delete a study"""
        study = model.Study.query.get(study_id)

        if not is_granted("delete_study", study):
            return "Access denied, you can not delete study", 403

        model.db.session.delete(study)
        model.db.session.commit()

        return Response(status=204)
