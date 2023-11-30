"""API endpoints for dataset funder"""
from typing import Any, Union

from flask import request, Response
from flask_restx import Resource, fields
from jsonschema import ValidationError, validate

import model
from apis.authentication import is_granted
from apis.dataset_metadata_namespace import api

dataset_funder = api.model(
    "DatasetFunder",
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


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/funder")
class DatasetFunderResource(Resource):
    """Dataset Funder Resource"""

    @api.doc("funder")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(dataset_funder)
    def get(self, study_id: int, dataset_id: int):  # pylint: disable= unused-argument
        """Get dataset funder"""
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_funder_ = dataset_.dataset_funder
        return [d.to_dict() for d in dataset_funder_], 200

    @api.doc("update funder")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def post(self, study_id: int, dataset_id: int):  # pylint: disable= unused-argument
        """Update dataset funder"""
        data: Union[Any, dict] = request.json
        study_obj = model.Study.query.get(study_id)

        if not is_granted("dataset_metadata", study_obj):
            return "Access denied, you can not make any change in dataset metadata", 403

        schema = {
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
        }

        try:
            validate(instance=request.json, schema=schema)
        except ValidationError as err:
            return err.message, 400

        data_obj = model.Dataset.query.get(dataset_id)
        list_of_elements = []
        for i in data:
            if "id" in i and i["id"]:
                dataset_funder_ = model.DatasetFunder.query.get(i["id"])
                if not dataset_funder_:
                    return f"Study link {i['id']} Id is not found", 404
                dataset_funder_.update(i)
                list_of_elements.append(dataset_funder_.to_dict())
            elif "id" not in i or not i["id"]:
                dataset_funder_ = model.DatasetFunder.from_data(data_obj, i)
                model.db.session.add(dataset_funder_)
                list_of_elements.append(dataset_funder_.to_dict())
        model.db.session.commit()
        return list_of_elements, 201


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/funder/<funder_id>")
class DatasetFunderUpdate(Resource):
    """Dataset Funder Update Resource"""

    @api.doc("delete funder")
    @api.response(200, "Success")
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
