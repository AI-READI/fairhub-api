from flask import Response, jsonify, request
from flask_restx import Namespace, Resource, fields

from model import Dataset, DatasetVersion, Participant, Study, db

api = Namespace("dataset", description="dataset operations", path="/")
dataset = api.model(
    "Dataset",
    {
        "id": fields.String(required=True),
        "name": fields.String(required=True),
        "title": fields.String(required=True),
        "description": fields.String(required=True),
    },
)

contributors = api.model(
    "DatasetVersion",
    {
        "id": fields.String(required=True),
        "affiliations": fields.String(required=True),
        "email": fields.String(required=True),
        "first_name": fields.String(required=True),
        "last_name": fields.String(required=True),
        "orcid": fields.String(required=True),
        "roles": fields.List(fields.String, required=True),
        "permission": fields.String(required=True),
        "status": fields.String(required=True),
    },
)

participants = api.model(
    "DatasetVersion",
    {
        "id": fields.Boolean(required=True),
        "first_name": fields.String(required=True),
        "last_name": fields.String(required=True),
        "address": fields.String(required=True),
        "age": fields.String(required=True),
    },
)


dataset_version = api.model(
    "Dataset",
    {
        "id": fields.String(required=True),
        "title": fields.String(required=True),
        "description": fields.String(required=True),
        "keywords": fields.String(required=True),
        "primary_language": fields.String(required=True),
        "modified": fields.DateTime(required=True),
        "published": fields.Boolean(required=True),
        "doi": fields.String(required=True),
        "name": fields.String(required=True),
        "contributors": fields.Nested(contributors, required=True),
        "participants": fields.Nested(participants, required=True),
    },
)


@api.route("/study/<study_id>/dataset")
class AddDataset(Resource):
    @api.response(201, "Success")
    @api.response(400, "Validation Error")
    @api.doc("dataset")
    @api.param("id", "Adding dataset")
    @api.marshal_with(dataset)
    def get(self, study_id):
        study = Study.query.get(study_id)
        datasets = Dataset.query.filter_by(study=study)
        return jsonify([d.to_dict() for d in datasets])

    @api.response(201, "Success")
    @api.response(400, "Validation Error")
    @api.doc("dataset")
    @api.param("id", "Adding dataset")
    @api.marshal_with(dataset)
    def post(self, study_id):
        data = request.json
        study = Study.query.get(study_id)
        # study_id
        # todo if study.participant id== different study Throw error
        # query based on part id and study id (prolly filter but need to find right syntax)
        # data["participants"] = [(Participant.filter_by(i="study_id".first()),Participant.filter_by
        # (i="participant_id".first()) )for i in data["participants"]]
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
    @api.doc("dataset version")
    @api.param("id", "Adding version")
    @api.marshal_with(dataset_version)
    def get(self, study_id, dataset_id, version_id):
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
class PostDatasetVersion(Resource):
    def post(self, study_id: int, dataset_id: int):
        data = request.json
        data["participants"] = [Participant.query.get(i) for i in data["participants"]]
        data_obj = Dataset.query.get(dataset_id)
        dataset_version = DatasetVersion.from_data(data_obj, data)
        db.session.add(dataset_version)
        db.session.commit()
        return jsonify(dataset_version.to_dict())


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

