from typing import Any, Union

from flask import request
from flask_restx import Resource, fields

import model
from apis.dataset_metadata_namespace import api

dataset_identifier = api.model(
    "DatasetAlternateIdentifier",
    {
        "id": fields.String(required=True),
        "identifier": fields.String(required=True),
        "identifier_type": fields.String(required=True),
        "alternate": fields.Boolean(required=True),
    },
)


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/identifier")
class DatasetAlternateIdentifierResource(Resource):
    @api.doc("identifier")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(dataset_identifier)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_identifier_ = dataset_.dataset_alternate_identifier
        return [d.to_dict() for d in dataset_identifier_]

    def post(self, study_id: int, dataset_id: int):
        data: Union[Any, dict] = request.json
        data_obj = model.Dataset.query.get(dataset_id)
        list_of_elements = []
        for i in data:
            if "id" in i and i["id"]:
                dataset_identifier_ = model.DatasetAlternateIdentifier.query.get(
                    i["id"]
                )
                if not dataset_identifier_:
                    return f"Study link {i['id']} Id is not found", 404
                dataset_identifier_.update(i)
                list_of_elements.append(dataset_identifier_.to_dict())
            elif "id" not in i or not i["id"]:
                dataset_identifier_ = model.DatasetAlternateIdentifier.from_data(
                    data_obj, i
                )
                model.db.session.add(dataset_identifier_)
                list_of_elements.append(dataset_identifier_.to_dict())
        model.db.session.commit()
        return list_of_elements

    @api.route(
        "/study/<study_id>/dataset/<dataset_id>/metadata/identifier/<identifier_id>"
    )
    class DatasetAlternateIdentifierUpdate(Resource):
        def put(self, study_id: int, dataset_id: int, identifier_id: int):
            dataset_identifier_ = model.DatasetAlternateIdentifier.query.get(
                identifier_id
            )
            dataset_identifier_.update(request.json)
            model.db.session.commit()
            return dataset_identifier_.to_dict()
