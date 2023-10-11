from flask import Response, jsonify, request
from flask_restx import Namespace, Resource, fields

from model import Dataset, Participant, Study, Version, db

from .authentication import is_granted

api = Namespace("Dataset", description="Dataset operations", path="/")


dataset_versions_model = api.model(
    "Version",
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
class DatasetList(Resource):
    @api.response(201, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(dataset)
    def get(self, study_id):
        study = Study.query.get(study_id)
        datasets = Dataset.query.filter_by(study=study)
        return [d.to_dict() for d in datasets]

    @api.response(201, "Success")
    @api.response(400, "Validation Error")
    @api.doc("update dataset")
    @api.expect(dataset)
    def post(self, study_id):
        study = Study.query.get(study_id)
        if not is_granted("add_dataset", study):
            return "Access denied, you can not modify", 403
        # todo if study.participant id== different study Throw error
        dataset_ = Dataset.from_data(study, request.json)
        db.session.add(dataset_)
        db.session.commit()
        return dataset_.to_dict()


# TODO not finalized endpoint. have to set functionality
@api.route("/study/<study_id>/dataset/<dataset_id>")
@api.response(201, "Success")
@api.response(400, "Validation Error")
class DatasetResource(Resource):
    @api.response(201, "Success")
    @api.response(400, "Validation Error")
    def get(self, study_id, dataset_id):
        data_obj = Dataset.query.get(dataset_id)
        return data_obj.to_dict()

    @api.response(201, "Success")
    @api.response(400, "Validation Error")
    def put(self, study_id, dataset_id):
        study = Study.query.get(study_id)
        if not is_granted("update_dataset", study):
            return "Access denied, you can not modify", 403
        data = request.json
        data_obj = Dataset.query.get(dataset_id)
        data_obj.update(data)
        db.session.commit()
        return data_obj.to_dict()

    @api.response(201, "Success")
    @api.response(400, "Validation Error")
    def delete(self, study_id, dataset_id):
        study = Study.query.get(study_id)
        if not is_granted("delete_dataset", study):
            return "Access denied, you can not modify", 403
        data_obj = Dataset.query.get(dataset_id)
        for version in data_obj.dataset_versions:
            db.session.delete(version)
        db.session.delete(data_obj)
        db.session.commit()
        dataset_ = study.dataset
        return [d.to_dict() for d in dataset_], 201

    # def delete(self, study_id, dataset_id, version_id):
    #     data_obj = Dataset.query.get(dataset_id)
    #     for version in data_obj.dataset_versions:
    #         db.session.delete(version)
    #         db.session.commit()
    #     db.session.delete(data_obj)
    #     db.session.commit()
    #     return Response(status=204)


@api.route("/study/<study_id>/dataset/<dataset_id>/version/<version_id>")
class VersionResource(Resource):
    @api.response(201, "Success")
    @api.response(400, "Validation Error")
    @api.doc("dataset version")
    @api.marshal_with(dataset_versions_model)
    def get(self, study_id, dataset_id, version_id):
        dataset_version = Version.query.get(version_id)
        return dataset_version.to_dict()

    def put(self, study_id, dataset_id, version_id):
        study = Study.query.get(study_id)
        if not is_granted("publish_dataset", study):
            return "Access denied, you can not modify", 403
        data_version_obj = Version.query.get(version_id)
        data_version_obj.update(request.json)
        db.session.commit()
        return jsonify(data_version_obj.to_dict()), 201

    def delete(self, study_id, dataset_id, version_id):
        study = Study.query.get(study_id)
        if not is_granted("delete_dataset", study):
            return "Access denied, you can not modify", 403
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
class VersionList(Resource):
    def post(self, study_id: int, dataset_id: int):
        study = Study.query.get(study_id)
        if not is_granted("publish_version", study):
            return "Access denied, you can not modify", 403
        data = request.json
        data["participants"] = [Participant.query.get(i) for i in data["participants"]]
        data_obj = Dataset.query.get(dataset_id)
        dataset_versions = Version.from_data(data_obj, data)
        db.session.add(dataset_versions)
        db.session.commit()
        return jsonify(dataset_versions.to_dict())
