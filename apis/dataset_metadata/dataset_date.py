from typing import Any, Union

from flask import request
from flask_restx import Resource, fields

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


@api.route("/study/<study_id>/dataset/<dataset_id>/date")
class DatasetDateResource(Resource):
    @api.doc("date")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(dataset_date)
    def get(self, study_id: int, dataset_id: int):  # pylint: disable= unused-argument
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_date_ = dataset_.dataset_date
        return [d.to_dict() for d in dataset_date_]

    @api.doc("update date")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def post(self, study_id: int, dataset_id: int):
        study_obj = model.Study.query.get(study_id)
        if not is_granted("dataset_metadata", study_obj):
            return "Access denied, you can not make any change in dataset metadata", 403
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


@api.route("/study/<study_id>/dataset/<dataset_id>/date/<date_id>")
class DatasetDateDeleteResource(Resource):
    @api.doc("delete date")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def delete(
        self, study_id: int, dataset_id: int, date_id: int
    ):  # pylint: disable= unused-argument
        study_obj = model.Study.query.get(study_id)
        if not is_granted("dataset_metadata", study_obj):
            return "Access denied, you can not make any change in dataset metadata", 403
        date_ = model.DatasetDate.query.get(date_id)

        model.db.session.delete(date_)
        model.db.session.commit()
        return 204
