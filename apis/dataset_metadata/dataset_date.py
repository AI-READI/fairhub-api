"""APIs for dataset date metadata"""
from typing import Any, Union

from flask import request
from flask_restx import Resource, fields
from jsonschema import ValidationError, validate

import model
from apis.authentication import is_granted
from apis.dataset_metadata_namespace import api

dataset_date = api.model(
    "DatasetDate",
    {
        "id": fields.String(required=True),
        "date": fields.String(required=True),
        "type": fields.String(required=True),
        "information": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/date")
class DatasetDateResource(Resource):
    """Dataset Date Resource"""

    @api.doc("date")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(dataset_date)
    def get(self, study_id: int, dataset_id: int):  # pylint: disable= unused-argument
        """Get dataset date"""
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_date_ = dataset_.dataset_date
        return [d.to_dict() for d in dataset_date_]

    @api.doc("update date")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def post(self, study_id: int, dataset_id: int):
        """Update dataset date"""
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
                    "date": {
                        "type": "integer",
                    },
                    "type": {
                        "type": "string",
                        "minLength": 1,
                    },
                    "information": {
                        "type": "string",
                    },
                },
                "required": ["date", "type", "information"],
            },
            "uniqueItems": True,
        }

        try:
            validate(instance=request.json, schema=schema)
        except ValidationError as err:
            return err.message, 400

        data: Union[Any, dict] = request.json
        data_obj = model.Dataset.query.get(dataset_id)
        list_of_elements = []
        for i in data:
            if "id" in i and i["id"]:
                dataset_date_ = model.DatasetDate.query.get(i["id"])
                if not dataset_date_:
                    return f"Study link {i['id']} Id is not found", 404
                dataset_date_.update(i)
                list_of_elements.append(dataset_date_.to_dict())
            elif "id" not in i or not i["id"]:
                dataset_date_ = model.DatasetDate.from_data(data_obj, i)
                model.db.session.add(dataset_date_)
                list_of_elements.append(dataset_date_.to_dict())
        model.db.session.commit()
        return list_of_elements


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/date/<date_id>")
class DatasetDateDeleteResource(Resource):
    """Dataset Date Delete Resource"""

    @api.doc("delete date")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def delete(
        self, study_id: int, dataset_id: int, date_id: int
    ):  # pylint: disable= unused-argument
        """Delete dataset date"""
        study_obj = model.Study.query.get(study_id)
        if not is_granted("dataset_metadata", study_obj):
            return "Access denied, you can not make any change in dataset metadata", 403
        date_ = model.DatasetDate.query.get(date_id)

        model.db.session.delete(date_)
        model.db.session.commit()
        return 204
