from flask import Response, jsonify, request
from flask_restx import Namespace, Resource

from model import Dataset, DatasetVersion, Participant, Study, db

api = Namespace("dataset", description="dataset operations", path="/")


@api.route("/study/<study_id>/dataset")
class AddDataset(Resource):
    @api.response(201, "Success")
    @api.response(400, "Validation Error")
    def get(self, study_id):
        study = Study.query.get(study_id)
        datasets = Dataset.query.filter_by(study=study)
        return jsonify([d.to_dict() for d in datasets])

    def post(self, study_id):
        data = request.json
        study = Study.query.get(study_id)
        # &&study_id
        # todo if study.participant id== different study Throw error
        # query based on part id and study id (prolly filter but need to find right syntax)
        data["participants"] = [
            Participant.query.get(i).first() for i in data["participants"]
        ]
        dataset_obj = Dataset(study)
        dataset_version = DatasetVersion.from_data(dataset_obj, data)
        db.session.add(dataset_obj)
        db.session.add(dataset_version)
        db.session.commit()
        return dataset_version.to_dict()


@api.route("/study/<study_id>/dataset/<dataset_id>/version/<version_id>")
class UpdateDataset(Resource):
    @api.response(201, "Success")
    @api.response(400, "Validation Error")
    def get(self, study_id, dataset_id, version_id):
        # if int(study_id) not in dic:
        #     return "not found", 404
        dataset_version = DatasetVersion.query.get(version_id)
        return jsonify(dataset_version.to_dict())

    def put(self, study_id, dataset_id, version_id):
        data_version_obj = DatasetVersion.query.get(version_id)
        data_version_obj.update(request.json)
        db.session.commit()
        return jsonify(data_version_obj.to_dict())

    def delete(self, study_id, dataset_id, version_id):
        data_obj = Dataset.query.get(dataset_id)
        for version in data_obj.dataset_versions:
            db.session.delete(version)
            db.session.commit()
        db.session.delete(data_obj)
        db.session.commit()
        return Response(status=204)


@api.route("/study/<study_id>/dataset/<dataset_id>/version")
@api.response(201, "Success")
@api.response(400, "Validation Error")
class PostDataset(Resource):
    def post(self, study_id: int, dataset_id: int):
        data = request.json
        data["participants"] = [Participant.query.get(i) for i in data["participants"]]
        data_obj = Dataset.query.get(dataset_id)
        dataset_version = DatasetVersion.from_data(data_obj, data)
        db.session.add(dataset_version)
        db.session.commit()
        return jsonify(dataset_version.to_dict())


# @dataset.route("/study/<study_id>/dataset/<dataset_id>", methods=["POST"])
# def update_dataset(study_id, dataset_id):
#     pass
#
