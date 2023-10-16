from typing import Union, Any

from flask import request
from flask_restx import Resource

import model
from apis.dataset_metadata_namespace import api

dataset_contributor = api.model(
    "DatasetContributor",
    {},
)


@api.route("/study/<study_id>/dataset/<dataset_id>/contributor")
class DatasetContributorResource(Resource):
    @api.doc("contributor")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(dataset_contributor)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_contributor_ = dataset_.dataset_contributors
        print("444444444444444444444444",[d.to_dict()["creator"] for d in dataset_contributor_ if d.to_dict()["creator"] == True])
        return [d.to_dict() for d in dataset_contributor_ if d.to_dict()["creator"] == False]

    @api.doc("update contributor")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def post(self, study_id: int, dataset_id: int):
        data: Union[Any, dict] = request.json
        data_obj = model.Dataset.query.get(dataset_id)
        list_of_elements = []
        for i in data:
            i["creator"] = False
            if "id" in i and i["id"]:
                dataset_contributor_ = model.DatasetContributor.query.get(
                    i["id"]
                )
                if not dataset_contributor_:
                    return f"Study link {i['id']} Id is not found", 404

                dataset_contributor_.update(i)
                list_of_elements.append(dataset_contributor_.to_dict())
            elif "id" not in i or not i["id"]:
                dataset_contributor_ = model.DatasetContributor.from_data(
                    data_obj, i
                )
                model.db.session.add(dataset_contributor_)
                list_of_elements.append(dataset_contributor_.to_dict())
        model.db.session.commit()
        return list_of_elements


@api.route("/study/<study_id>/dataset/<dataset_id>/contributor/<contributor_id>")
class DatasetContributorDelete(Resource):
    @api.doc("delete contributor")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def delete(self, study_id: int, dataset_id: int, contributor_id: int):
        contributor_ = model.DatasetContributor.query.get(contributor_id)

        model.db.session.delete(contributor_)
        model.db.session.commit()

        return 204


@api.route("/study/<study_id>/dataset/<dataset_id>/creator")
class DatasetContributorResource(Resource):
    @api.doc("creator")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(dataset_contributor)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_creator_ = dataset_.dataset_contributors
        return [d.to_dict() for d in dataset_creator_ if d.to_dict()["creator"] == True]

    @api.doc("update creator")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def post(self, study_id: int, dataset_id: int):
        data: Union[Any, dict] = request.json
        data_obj = model.Dataset.query.get(dataset_id)
        list_of_elements = []
        for i in data:

            i["creator"] = True

            if "id" in i and i["id"]:
                dataset_creator_ = model.DatasetContributor.query.get(
                    i["id"]
                )
                if not dataset_creator_:
                    return f"Study link {i['id']} Id is not found", 404
                dataset_creator_.update(i)
                list_of_elements.append(dataset_creator_.to_dict())
            elif "id" not in i or not i["id"]:
                dataset_creator_ = model.DatasetContributor.from_data(
                    data_obj, i
                )
                model.db.session.add(dataset_creator_)
                list_of_elements.append(dataset_creator_.to_dict())
        model.db.session.commit()
        return list_of_elements
