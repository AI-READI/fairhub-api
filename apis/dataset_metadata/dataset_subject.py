from typing import Any, Union

from flask import request
from flask_restx import Resource, fields

import model
from apis.dataset_metadata_namespace import api

dataset_subject = api.model(
    "DatasetSubject",
    {
        "id": fields.String(required=True),
        "subject": fields.String(required=True),
        "scheme": fields.String(required=True),
        "scheme_uri": fields.String(required=True),
        "value_uri": fields.String(required=True),
        "classification_code": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/dataset/<dataset_id>/subject")
class DatasetSubjectResource(Resource):
    @api.doc("subject")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The dataset identifier")
    @api.marshal_with(dataset_subject)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_subject_ = dataset_.dataset_subject
        return [d.to_dict() for d in dataset_subject_]

    @api.doc("update subject")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def post(self, study_id: int, dataset_id: int):
        data: Union[Any, dict] = request.json
        data_obj = model.Dataset.query.get(dataset_id)
        list_of_elements = []
        for i in data:
            if "id" in i and i["id"]:
                dataset_subject_ = model.DatasetSubject.query.get(
                    i["id"])
                if not dataset_subject_:
                    return f"Study link {i['id']} Id is not found", 404
                dataset_subject_.update(i)
                list_of_elements.append(dataset_subject_.to_dict())
            elif "id" not in i or not i["id"]:
                dataset_subject_ = model.DatasetSubject.from_data(
                    data_obj, i)
                model.db.session.add(dataset_subject_)
                list_of_elements.append(dataset_subject_.to_dict())
        model.db.session.commit()
        return list_of_elements


@api.route("/study/<study_id>/dataset/<dataset_id>/subject/<subject_id>")
class DatasetSubjectUpdate(Resource):
    @api.doc("delete subject")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def delete(self, study_id: int, dataset_id: int, subject_id: int):
        dataset_subject_ = model.DatasetSubject.query.get(subject_id)

        model.db.session.delete(dataset_subject_)
        model.db.session.commit()

        return 204
