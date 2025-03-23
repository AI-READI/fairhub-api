"""API for dataset contributor metadata"""

from typing import Any, Union

from flask import Response, request
from flask_restx import Resource, fields
from jsonschema import ValidationError, validate

import model
from apis.authentication import is_granted
from apis.dataset_metadata_namespace import api

dataset_team = api.model(
    "DatasetTeam",
    {
        "contributors": fields.List(
            fields.Nested(
                api.model(
                    "Contributor",
                    {
                        "id": fields.String(required=True),
                        "family_name": fields.String(),
                        "given_name": fields.String(required=True),
                        "name_type": fields.String(),
                        "name_identifier": fields.String(required=True),
                        "name_identifier_scheme": fields.String(required=True),
                        "name_identifier_scheme_uri": fields.String(required=True),
                        "creator": fields.Boolean(required=True),
                        "contributor_type": fields.String(),
                        "affiliations": fields.Raw(required=True),
                        "created_at": fields.Integer(required=True),
                    },
                )
            )
        ),
        "creators": fields.List(
            fields.Nested(
                api.model(
                    "Creator",
                    {
                        "id": fields.String(required=True),
                        "family_name": fields.String(),
                        "given_name": fields.String(required=True),
                        "name_type": fields.String(),
                        "name_identifier": fields.String(required=True),
                        "name_identifier_scheme": fields.String(required=True),
                        "name_identifier_scheme_uri": fields.String(required=True),
                        "creator": fields.Boolean(required=True),
                        "contributor_type": fields.String(),
                        "affiliations": fields.Raw(required=True),
                        "created_at": fields.Integer(required=True),
                    },
                )
            )
        ),
        "managing_organization": fields.Nested(
            api.model(
                "DatasetManagingOrganization",
                {
                    "name": fields.String(required=True),
                    "identifier": fields.String(required=True),
                    "identifier_scheme": fields.String(required=True),
                    "identifier_scheme_uri": fields.String(required=True),
                },
            )
        ),
        "funders": fields.List(
            fields.Nested(
                api.model(
                    "Funders",
                    {
                        "id": fields.String(required=True),
                        "name": fields.String(required=True),
                        "identifier": fields.String(required=True),
                        "identifier_type": fields.String(required=True),
                        "identifier_scheme_uri": fields.String(required=True),
                        "award_number": fields.String(required=True),
                        "award_uri": fields.String(required=True),
                        "award_title": fields.String(required=True),
                    },
                )
            )
        ),
    },
)


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/team")
class DatasetTeamResource(Resource):
    """Dataset Team Resource"""

    @api.doc("team")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(dataset_team)
    def get(self, study_id: int, dataset_id: int):  # pylint: disable= unused-argument
        """Get dataset creator"""
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_creator_ = dataset_.dataset_contributors
        dataset_contributor_ = dataset_.dataset_contributors
        dataset_funder_ = dataset_.dataset_funder
        managing_organization_ = dataset_.dataset_managing_organization
        return {
            "creators": [
                d.to_dict() for d in dataset_creator_ if d.to_dict()["creator"]
            ],
            "contributors": [
                d.to_dict() for d in dataset_contributor_ if not d.to_dict()["creator"]
            ],
            "managing_organization": managing_organization_.to_dict(),
            "funders": [d.to_dict() for d in dataset_funder_],
        }, 200

    @api.doc("update team")
    @api.response(201, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(dataset_team)
    def post(self, study_id: int, dataset_id: int):
        """Update dataset team"""
        study_obj = model.Study.query.get(study_id)

        if not is_granted("dataset_metadata", study_obj):
            return "Access denied, you can not make any change in dataset metadata", 403

        schema = {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "creators": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "id": {"type": "string"},
                            "given_name": {"type": "string", "minLength": 1},
                            "family_name": {"type": ["string", "null"]},
                            "name_identifier": {"type": "string", "minLength": 1},
                            "name_identifier_scheme": {
                                "type": "string",
                                "minLength": 1,
                            },
                            "name_identifier_scheme_uri": {"type": "string"},
                            "name_type": {
                                "type": "string",
                                "enum": ["Personal", "Organizational"],
                                "minLength": 1,
                            },
                            "affiliations": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "additionalProperties": False,
                                    "properties": {
                                        "name": {"type": "string"},
                                        "identifier": {"type": "string"},
                                        "scheme": {"type": "string"},
                                        "scheme_uri": {"type": "string"},
                                    },
                                },
                                "uniqueItems": True,
                            },
                        },
                        "required": [
                            "name_type",
                            "given_name",
                            "affiliations",
                            "name_identifier",
                            "name_identifier_scheme",
                        ],
                    },
                },
                "contributors": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "id": {"type": "string"},
                            "contributor_type": {"type": "string", "minLength": 1},
                            "given_name": {"type": "string", "minLength": 1},
                            "family_name": {"type": ["string", "null"]},
                            "name_identifier": {"type": "string", "minLength": 1},
                            "name_identifier_scheme": {
                                "type": "string",
                                "minLength": 1,
                            },
                            "name_identifier_scheme_uri": {"type": "string"},
                            "name_type": {
                                "type": "string",
                                "enum": ["Personal", "Organizational"],
                                "minLength": 1,
                            },
                            "affiliations": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "additionalProperties": False,
                                    "properties": {
                                        "name": {"type": "string"},
                                        "identifier": {"type": "string"},
                                        "scheme": {"type": "string"},
                                        "scheme_uri": {"type": "string"},
                                    },
                                },
                                "uniqueItems": True,
                            },
                        },
                        "required": [
                            "contributor_type",
                            "name_type",
                            "given_name",
                            "affiliations",
                            "name_identifier",
                            "name_identifier_scheme",
                        ],
                    },
                },
                "funders": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "id": {"type": "string"},
                            "name": {"type": "string", "minLength": 1},
                            "award_number": {"type": "string", "minLength": 1},
                            "award_title": {"type": "string"},
                            "award_uri": {"type": "string"},
                            "identifier": {"type": "string", "minLength": 1},
                            "identifier_scheme_uri": {"type": "string"},
                            "identifier_type": {"type": ["string", "null"]},
                        },
                        "required": [
                            "name",
                            "award_number",
                            "award_title",
                            "award_uri",
                            "identifier",
                            "identifier_scheme_uri",
                            "identifier_type",
                        ],
                    },
                    "uniqueItems": True,
                },
                "managing_organization": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "name": {"type": "string", "minLength": 1},
                        "identifier": {"type": "string"},
                        "identifier_scheme": {"type": "string"},
                        "identifier_scheme_uri": {"type": "string"},
                    },
                    "required": [
                        "name",
                        "identifier",
                        "identifier_scheme",
                        "identifier_scheme_uri",
                    ],
                },
            },
            "required": [
                "creators",
                "contributors",
                "funders",
                "managing_organization",
            ],
        }

        try:
            validate(request.json, schema)
        except ValidationError as e:
            return e.message, 400

        data: Union[Any, dict] = request.json
        data_obj = model.Dataset.query.get(dataset_id)

        list_of_creator = []
        for i in data["creators"]:
            i["creator"] = True
            if "id" in i and i["id"]:
                i["contributor_type"] = None
                dataset_creator_ = model.DatasetContributor.query.get(i["id"])
                if not dataset_creator_:
                    return f"Study link {i['id']} Id is not found", 404
                dataset_creator_.update(i)
                list_of_creator.append(dataset_creator_.to_dict())
            elif "id" not in i or not i["id"]:
                i["contributor_type"] = None
                dataset_creator_ = model.DatasetContributor.from_data(data_obj, i)
                model.db.session.add(dataset_creator_)
                list_of_creator.append(dataset_creator_.to_dict())

        list_of_contributors = []
        for i in data["contributors"]:
            i["creator"] = False
            if "id" in i and i["id"]:
                dataset_contributor_ = model.DatasetContributor.query.get(i["id"])
                if not dataset_contributor_:
                    return f"Study link {i['id']} Id is not found", 404
                dataset_contributor_.update(i)
                list_of_contributors.append(dataset_contributor_.to_dict())
            elif "id" not in i or not i["id"]:
                dataset_contributor_ = model.DatasetContributor.from_data(data_obj, i)
                model.db.session.add(dataset_contributor_)
                list_of_contributors.append(dataset_contributor_.to_dict())

        list_of_funders = []
        for i in data["funders"]:
            if "id" in i and i["id"]:
                dataset_funder_ = model.DatasetFunder.query.get(i["id"])
                if not dataset_funder_:
                    return f"Study link {i['id']} Id is not found", 404
                dataset_funder_.update(i)
                list_of_funders.append(dataset_funder_.to_dict())
            elif "id" not in i or not i["id"]:
                dataset_funder_ = model.DatasetFunder.from_data(data_obj, i)
                print("herereeeeeeee", dataset_funder_.to_dict())
                model.db.session.add(dataset_funder_)
                list_of_funders.append(dataset_funder_.to_dict())

        data_obj.dataset_managing_organization.update(data["managing_organization"])
        model.db.session.commit()
        return {
            "creators": list_of_creator,
            "contributors": list_of_contributors,
            "managing_organization": data_obj.dataset_managing_organization.to_dict(),
            "funders": list_of_funders,
        }, 200


@api.route(
    "/study/<study_id>/dataset/<dataset_id>/metadata/contributor/<contributor_id>"
)
class DatasetContributorDelete(Resource):
    """Dataset Contributor Delete Resource"""

    @api.doc("delete contributor")
    @api.response(204, "Success")
    @api.response(400, "Validation Error")
    def delete(
        self,
        study_id: int,
        dataset_id: int,  # pylint: disable= unused-argument
        contributor_id: int,
    ):
        """Delete dataset contributor"""
        study_obj = model.Study.query.get(study_id)
        if not is_granted("dataset_metadata", study_obj):
            return "Access denied, you can not make any change in dataset metadata", 403
        contributor_ = model.DatasetContributor.query.get(contributor_id)

        model.db.session.delete(contributor_)
        model.db.session.commit()

        return Response(status=204)


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/creator/<creator_id>")
class DatasetCreatorDelete(Resource):
    @api.doc("delete creator")
    @api.response(204, "Success")
    @api.response(400, "Validation Error")
    def delete(
        self,
        study_id: int,
        dataset_id: int,  # pylint: disable= unused-argument
        creator_id: int,
    ):
        """Delete dataset creator"""
        study_obj = model.Study.query.get(study_id)
        if not is_granted("dataset_metadata", study_obj):
            return "Access denied, you can not make any change in dataset metadata", 403
        dataset_creator_ = model.DatasetContributor.query.get(creator_id)
        model.db.session.delete(dataset_creator_)
        model.db.session.commit()

        return Response(status=204)


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/funder/<funder_id>")
class DatasetFunderUpdate(Resource):
    """Dataset Funder Update Resource"""

    @api.doc("delete funder")
    @api.response(204, "Success")
    @api.response(400, "Validation Error")
    def delete(
        self,
        study_id: int,
        dataset_id: int,  # pylint: disable= unused-argument
        funder_id: int,
    ):
        """Delete dataset funder"""
        study_obj = model.Study.query.get(study_id)
        if not is_granted("dataset_metadata", study_obj):
            return "Access denied, you can not make any change in dataset metadata", 403
        dataset_funder_ = model.DatasetFunder.query.get(funder_id)

        model.db.session.delete(dataset_funder_)
        model.db.session.commit()

        return Response(status=204)
