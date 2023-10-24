from typing import Any, Union

from flask import request
from flask_restx import Resource

import model
from apis.authentication import is_granted
from apis.dataset_metadata_namespace import api

dataset_contributor = api.model(
    "DatasetContributor",
    {},
)


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/contributor")
class DatasetContributorResource(Resource):
    @api.doc("contributor")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(dataset_contributor)
    def get(self, study_id: int, dataset_id: int):  # pylint: disable= unused-argument
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_contributor_ = dataset_.dataset_contributors
        return [d.to_dict() for d in dataset_contributor_ if not d.to_dict()["creator"]]

    @api.doc("update contributor")
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
            i["creator"] = False
            if "id" in i and i["id"]:
                dataset_contributor_ = model.DatasetContributor.query.get(i["id"])
                if not dataset_contributor_:
                    return f"Study link {i['id']} Id is not found", 404
                dataset_contributor_.update(i)
                list_of_elements.append(dataset_contributor_.to_dict())
            elif "id" not in i or not i["id"]:
                dataset_contributor_ = model.DatasetContributor.from_data(data_obj, i)
                model.db.session.add(dataset_contributor_)
                list_of_elements.append(dataset_contributor_.to_dict())
        model.db.session.commit()
        return list_of_elements


@api.route("/study/<study_id>/dataset/<dataset_id>/"
           "metadata/contributor/<contributor_id>")
class DatasetContributorDelete(Resource):
    @api.doc("delete contributor")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def delete(
        self,
        study_id: int,
        dataset_id: int,  # pylint: disable= unused-argument
        contributor_id: int,
    ):
        study_obj = model.Study.query.get(study_id)
        if not is_granted("dataset_metadata", study_obj):
            return "Access denied, you can not make any change in dataset metadata", 403
        contributor_ = model.DatasetContributor.query.get(contributor_id)

        model.db.session.delete(contributor_)
        model.db.session.commit()

        return 204


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/creator")
class DatasetCreatorResource(Resource):
    @api.doc("creator")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(dataset_contributor)
    def get(self, study_id: int, dataset_id: int):  # pylint: disable= unused-argument
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_creator_ = dataset_.dataset_contributors
        return [d.to_dict() for d in dataset_creator_ if d.to_dict()["creator"]]

    @api.doc("update creator")
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
            i["creator"] = True
            if "id" in i and i["id"]:
                dataset_creator_ = model.DatasetContributor.query.get(i["id"])
                if not dataset_creator_:
                    return f"Study link {i['id']} Id is not found", 404
                dataset_creator_.update(i)
                list_of_elements.append(dataset_creator_.to_dict())
            elif "id" not in i or not i["id"]:
                i["contributor_type"] = None
                dataset_creator_ = model.DatasetContributor.from_data(data_obj, i)
                model.db.session.add(dataset_creator_)
                list_of_elements.append(dataset_creator_.to_dict())
        model.db.session.commit()
        return list_of_elements


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/creator/<creator_id>")
class DatasetCreatorDelete(Resource):
    @api.doc("delete creator")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def delete(
        self,
        study_id: int,
        dataset_id: int,  # pylint: disable= unused-argument
        creator_id: int,
    ):
        study_obj = model.Study.query.get(study_id)
        if not is_granted("dataset_metadata", study_obj):
            return "Access denied, you can not make any change in dataset metadata", 403
        dataset_creator_ = model.DatasetContributor.query.get(creator_id)
        model.db.session.delete(dataset_creator_)
        model.db.session.commit()

        return 204
