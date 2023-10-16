from typing import Any, Union

from flask import request
from flask_restx import Resource, fields

import model
from apis.dataset_metadata_namespace import api

dataset_title = api.model(
    "DatasetTitle",
    {
        "id": fields.String(required=True),
        "title": fields.String(required=True),
        "type": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/dataset/<dataset_id>/title")
class DatasetTitleResource(Resource):
    @api.doc("title")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The dataset identifier")
    @api.marshal_with(dataset_title)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_title_ = dataset_.dataset_title
        return [d.to_dict() for d in dataset_title_]

    @api.doc("update title")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def post(self, study_id: int, dataset_id: int):
        data: Union[Any, dict] = request.json
        data_obj = model.Dataset.query.get(dataset_id)
        list_of_elements = []
        for i in data:
            if "id" in i and i["id"]:
                dataset_title_ = model.DatasetTitle.query.get(i["id"])
                dataset_title_.update(i)
                list_of_elements.append(dataset_title_.to_dict())
            elif "id" not in i or not i["id"]:
                dataset_title_ = model.DatasetTitle.from_data(data_obj, i)
                model.db.session.add(dataset_title_)
                list_of_elements.append(dataset_title_.to_dict())
        model.db.session.commit()
        return list_of_elements

    @api.route("/study/<study_id>/dataset/<dataset_id>/title/<title_id>")
    class DatasetDescriptionUpdate(Resource):
        @api.doc("delete title")
        @api.response(200, "Success")
        @api.response(400, "Validation Error")
        def delete(self, study_id: int, dataset_id: int, title_id: int):
            dataset_title_ = model.DatasetTitle.query.get(title_id)
            model.db.session.delete(dataset_title_)
            model.db.session.commit()
            return 204
