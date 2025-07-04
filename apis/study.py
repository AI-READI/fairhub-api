"""APIs for study operations""" ""
import os
import re
from typing import Any, Union

import requests
from azure.storage.filedatalake import FileSystemClient
from flask import Response, g, request
from flask_restx import Namespace, Resource, fields, reqparse
from jsonschema import FormatChecker, ValidationError, validate

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

    @api.expect(study_model)
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
        identifier = data["clinical_id"]

        def validate_clinical_trial_identifier(instance):
            identifier_ = instance
            if not identifier_:
                return True

            # Check if the identifier is exactly 11 characters long
            if len(identifier_) != 11:
                raise ValidationError("Identifier must be exactly 11 characters long")

            # Check if it starts with 'NCT' followed by 8 digits
            if not re.fullmatch(r"NCT\d{8}", identifier_):
                raise ValidationError(
                    "Identifier must start with 'NCT' followed by 8 digits"
                )

            return True

        format_checker = FormatChecker()
        format_checker.checks("clinical_id")(validate_clinical_trial_identifier)

        try:
            validate(instance=data, schema=schema, format_checker=format_checker)
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
            if identifier:
                try:
                    url = f"https://classic.clinicaltrials.gov/api/v2/studies/{identifier}"
                    assert url is not None and isinstance(
                        url, str
                    ), "URL must be a non-empty string"

                    response = requests.get(url, timeout=10)
                    response.raise_for_status()  # Raises HTTPError if status != 200
                    clinical_data = response.json()
                    study_.update_identification_id(clinical_data["protocolSection"])

                    study_.import_from_clinical_data(clinical_data["protocolSection"])
                    print("Response JSON")

                except requests.exceptions.RequestException as e:
                    print(f"Request error: {e}")
                except Exception as e:
                    print(f"Unexpected error: {e}")

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
                url = f"https://classic.clinicaltrials.gov/api/v2/studies/{identifier}"
                # AI-READI id-NCT06002048
                assert url is not None and isinstance(
                    url, str
                ), "URL must be a non-empty string"

                response = requests.get(url, timeout=10)
                response.raise_for_status()  # Raises HTTPError if status != 200
                clinical_data = response.json()
                update_study.update_identification_id(clinical_data["protocolSection"])
                if is_overwrite:
                    update_study.import_from_clinical_data(
                        clinical_data["protocolSection"]
                    )

            except requests.exceptions.RequestException as e:
                print(f"Request error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

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
