"""API for dataset title metadata"""
from typing import Any, Union

from flask import request
from flask_restx import Resource, fields
from jsonschema import ValidationError, validate

import model
from apis.authentication import is_granted
from apis.dataset_metadata_namespace import api

dataset_title = api.model(
    "DatasetTitle",
    {
        "id": fields.String(required=True),
        "title": fields.String(required=True),
        "type": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/title")
class DatasetTitleResource(Resource):
    """Dataset Title Resource"""

    @api.doc("title")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The dataset identifier")
    @api.marshal_with(dataset_title)
    def get(self, study_id: int, dataset_id: int):  # pylint: disable= unused-argument
        """Get dataset title"""
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_title_ = dataset_.dataset_title
        return [d.to_dict() for d in dataset_title_]

    @api.doc("update title")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def post(self, study_id: int, dataset_id: int):
        """Update dataset title"""
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
                    "title": {
                        "type": "string",
                        "minLength": 1,
                    },
                    "type": {
                        "type": "string",
                        "enum": [
                            "MainTitle",
                            "AlternativeTitle",
                            "Subtitle",
                            "TranslatedTitle",
                            "OtherTitle",
                            "MainTitle",
                        ],
                    },
                },
                "required": ["title", "type"],
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
                dataset_title_ = model.DatasetTitle.query.get(i["id"])
                # if dataset_title_.type == "Main Title":
                #     return (
                #         "Main Title type can not be modified",
                #         403,
                #
                dataset_title_.update(i)
                list_of_elements.append(dataset_title_.to_dict())
            elif "id" not in i or not i["id"]:
                if i["type"] == "Main Title":
                    return (
                        "Main Title type can not be given",
                        403,
                    )
                dataset_title_ = model.DatasetTitle.from_data(data_obj, i)
                model.db.session.add(dataset_title_)
                list_of_elements.append(dataset_title_.to_dict())
        model.db.session.commit()
        return list_of_elements

    @api.route("/study/<study_id>/dataset/<dataset_id>/metadata/title/<title_id>")
    class DatasetDescriptionUpdate(Resource):
        """Dataset Title Update Resource"""

        @api.doc("delete title")
        @api.response(200, "Success")
        @api.response(400, "Validation Error")
        def delete(
            self,
            study_id: int,
            dataset_id: int,  # pylint: disable= unused-argument
            title_id: int,
        ):
            """Delete dataset title"""
            study_obj = model.Study.query.get(study_id)
            if not is_granted("dataset_metadata", study_obj):
                return (
                    "Access denied, you can not make any change in dataset metadata",
                    403,
                )
            dataset_title_ = model.DatasetTitle.query.get(title_id)
            if dataset_title_.type == "Main Title":
                return (
                    "Main Title type can not be deleted",
                    403,
                )
            model.db.session.delete(dataset_title_)
            model.db.session.commit()
            return 204
