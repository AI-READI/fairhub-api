from model import Dataset, db, DatasetDescription

from flask_restx import Resource, fields
from flask import request


from apis.dataset_metadata_namespace import api

dataset_description = api.model(
    "DatasetDescription",
    {
        "id": fields.String(required=True),
        "description": fields.String(required=True),
        "description_type": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/description")
class DatasetDescriptionResource(Resource):
    @api.doc("description")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(dataset_description)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = Dataset.query.get(dataset_id)
        dataset_description_ = dataset_.dataset_description
        return [d.to_dict() for d in dataset_description_]

    def post(self, study_id: int, dataset_id: int):
        data = request.json
        data_obj = Dataset.query.get(dataset_id)
        list_of_elements = []
        for i in data:
            if "id" in i and i["id"]:
                dataset_description_ = DatasetDescription.query.get(i["id"])
                dataset_description_.update(i)
                list_of_elements.append(dataset_description_.to_dict())
            elif "id" not in i or not i["id"]:
                dataset_description_ = DatasetDescription.from_data(data_obj, i)
                db.session.add(dataset_description_)
                list_of_elements.append(dataset_description_.to_dict())
        db.session.commit()
        return list_of_elements

    @api.route(
        "/study/<study_id>/dataset/<dataset_id>/metadata/description/<description_id>"
    )
    class DatasetDescriptionUpdate(Resource):
        def delete(self, study_id: int, dataset_id: int, description_id: int):
            dataset_description_ = DatasetDescription.query.get(description_id)
            db.session.delete(dataset_description_)
            db.session.commit()
            return dataset_description_.to_dict()
