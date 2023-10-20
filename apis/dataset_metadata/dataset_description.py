from typing import Any, Union

from apis.authentication import is_granted
from flask import request
from flask_restx import Resource, fields

import model
from apis.dataset_metadata_namespace import api

dataset_description = api.model(
    "DatasetDescription",
    {
        "id": fields.String(required=True),
        "description": fields.String(required=True),
        "description_type": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/dataset/<dataset_id>/description")
class DatasetDescriptionResource(Resource):
    @api.doc("description")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(dataset_description)
    def get(self, study_id: int, dataset_id: int):  # pylint: disable= unused-argument
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_description_ = dataset_.dataset_description
        return [d.to_dict() for d in dataset_description_]

    @api.doc("update description")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(dataset_description)
    def post(self, study_id: int, dataset_id: int):
        study_obj = model.Study.query.get(study_id)
        if not is_granted("dataset_metadata", study_obj):
            return "Access denied, you can not make any change in dataset metadata", 403
        data: Union[Any, dict] = request.json
        data_obj = model.Dataset.query.get(dataset_id)
        list_of_elements = []
        for i in data:
            if "id" in i and i["id"]:
                dataset_description_ = model.DatasetDescription.query.get(i["id"])
                dataset_description_.update(i)
                list_of_elements.append(dataset_description_.to_dict())
            elif "id" not in i or not i["id"]:
                dataset_description_ = model.DatasetDescription.from_data(data_obj, i)
                model.db.session.add(dataset_description_)
                list_of_elements.append(dataset_description_.to_dict())
        model.db.session.commit()
        return list_of_elements

    @api.route("/study/<study_id>/dataset/<dataset_id>/description/<description_id>")
    class DatasetDescriptionUpdate(Resource):
        @api.doc("delete description")
        @api.response(200, "Success")
        @api.response(400, "Validation Error")
        def delete(
            self,
            study_id: int,
            dataset_id: int,  # pylint: disable= unused-argument
            description_id: int,
        ):
            study_obj = model.Study.query.get(study_id)
            if not is_granted("dataset_metadata", study_obj):
                return "Access denied, you can not make any change in dataset metadata", 403
            dataset_description_ = model.DatasetDescription.query.get(description_id)

            model.db.session.delete(dataset_description_)
            model.db.session.commit()

            return 204
