from typing import Any, Union

from flask import request
from flask_restx import Resource, fields

import model
from apis.dataset_metadata_namespace import api

dataset_rights = api.model(
    "DatasetRights",
    {
        "id": fields.String(required=True),
        "rights": fields.String(required=True),
        "uri": fields.String(required=True),
        "identifier": fields.String(required=True),
        "identifier_scheme": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/dataset/<dataset_id>/rights")
class DatasetRightsResource(Resource):
    @api.doc("rights")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The dataset identifier")
    @api.marshal_with(dataset_rights)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_rights_ = dataset_.dataset_rights
        return [d.to_dict() for d in dataset_rights_]

    @api.doc("update rights")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def post(self, study_id: int, dataset_id: int):
        data: Union[Any, dict] = request.json
        data_obj = model.Dataset.query.get(dataset_id)
        list_of_elements = []
        for i in data:
            if "id" in i and i["id"]:
                dataset_rights_ = model.DatasetRights.query.get(
                    i["id"])
                if not dataset_rights_:
                    return f"Study link {i['id']} Id is not found", 404
                dataset_rights_.update(i)
                list_of_elements.append(dataset_rights_.to_dict())
            elif "id" not in i or not i["id"]:
                dataset_rights_ = model.DatasetRights.from_data(
                    data_obj, i)
                model.db.session.add(dataset_rights_)
                list_of_elements.append(dataset_rights_.to_dict())
        model.db.session.commit()
        return list_of_elements


@api.route("/study/<study_id>/dataset/<dataset_id>/rights/<rights_id>")
class DatasetRightsUpdate(Resource):
    @api.doc("delete rights")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def delete(self, study_id: int, dataset_id: int, rights_id: int):
        dataset_rights_ = model.DatasetRights.query.get(rights_id)

        model.db.session.delete(dataset_rights_)
        model.db.session.commit()

        return 204
