from flask import Response, jsonify, request
from flask_restx import Namespace, Resource, fields

from model import Dataset, DatasetVersion, Participant, Study, db

api = Namespace("dataset", description="dataset operations", path="/")


dataset_versions_model = api.model(
    "DatasetVersion",
    {
        "id": fields.String(required=True),
        "title": fields.String(required=True),
        "changelog": fields.String(required=True),
        "created_at": fields.String(required=True),
        "doi": fields.String(required=True),
        "published": fields.Boolean(required=True),
        "participants": fields.List(fields.String, required=True),
        "published_on": fields.String(required=True),
    },
)

dataset = api.model(
    "Dataset",
    {
        "id": fields.String(required=True),
        "updated_on": fields.String(required=True),
        "created_at": fields.String(required=True),
        "dataset_versions": fields.Nested(dataset_versions_model, required=True),
        "latest_version": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/dataset")
class AddDataset(Resource):
    @api.response(201, "Success")
    @api.response(400, "Validation Error")
    @api.doc("add dataset", params={"id": "An ID"})
    @api.marshal_with(dataset)
    # @api.expect(body=dataset)
    def get(self, study_id):
        study = Study.query.get(study_id)
        datasets = Dataset.query.filter_by(study=study)
        return [d.to_dict() for d in datasets]

    @api.response(201, "Success")
    @api.response(400, "Validation Error")
    @api.doc("update dataset")
    @api.marshal_with(dataset)
    def post(self, study_id):
        data = request.json
        study = Study.query.get(study_id)
        # todo if study.participant id== different study Throw error
        dataset_obj = Dataset(study)
        dataset_versions = DatasetVersion.from_data(dataset_obj, data)
        db.session.add(dataset_obj)
        db.session.add(dataset_versions)
        db.session.commit()
        return dataset_versions.to_dict()


@api.route("/study/<study_id>/dataset/<dataset_id>/version/<version_id>")
class UpdateDataset(Resource):
    @api.response(201, "Success")
    @api.response(400, "Validation Error")
    @api.doc("dataset version")
    @api.param("id", "Adding version")
    @api.marshal_with(dataset_versions_model)
    def get(self, study_id, dataset_id, version_id):
        dataset_version = DatasetVersion.query.get(version_id)
        return dataset_version.to_dict()

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
class PostDatasetVersion(Resource):
    def post(self, study_id: int, dataset_id: int):
        data = request.json
        data["participants"] = [Participant.query.get(i) for i in data["participants"]]
        data_obj = Dataset.query.get(dataset_id)
        dataset_versions = DatasetVersion.from_data(data_obj, data)
        db.session.add(dataset_versions)
        db.session.commit()
        return jsonify(dataset_versions.to_dict())


# TODO not finalized endpoint. have to set functionality
@api.route("/study/<study_id>/dataset/<dataset_id>")
@api.response(201, "Success")
@api.response(400, "Validation Error")
class PostDataset(Resource):
    def put(study_id, dataset_id):
        data = request.json
        data["participants"] = [Participant.query.get(i) for i in data["participants"]]
        data_obj = Dataset.query.get(dataset_id)
        dataset_ = Dataset.from_data(data_obj, data)
        db.session.add(dataset_)
        db.session.commit()
        return jsonify(dataset_.to_dict())
