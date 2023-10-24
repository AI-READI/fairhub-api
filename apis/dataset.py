import typing

from flask import Response, jsonify, request
from flask_restx import Namespace, Resource, fields

import model

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
        study = model.Study.query.get(study_id)
        datasets = model.Dataset.query.filter_by(study=study)
        return [d.to_dict() for d in datasets]

    @api.response(201, "Success")
    @api.response(400, "Validation Error")
    @api.doc("update dataset")
    @api.expect(dataset)
    def post(self, study_id):
        study = model.Study.query.get(study_id)
        if not is_granted("add_dataset", study):
            return "Access denied, you can not modify", 403
        # todo if study.participant id== different study Throw error
        data: typing.Union[typing.Any, dict] = request.json
        dataset_ = model.Dataset.from_data(study)
        model.db.session.add(dataset_)

        title_element = model.DatasetTitle.query.filter_by(
            dataset_id=dataset_.id
        ).first()
        title_element.title = data["title"]

        description_element = model.DatasetDescription.query.filter_by(
            dataset_id=dataset_.id
        ).first()
        description_element.description = data["description"]

        model.db.session.commit()
        return dataset_.to_dict()


# TODO not finalized endpoint. have to set functionality
@api.route("/study/<study_id>/dataset/<dataset_id>")
@api.response(201, "Success")
@api.response(400, "Validation Error")
class DatasetResource(Resource):
    @api.response(201, "Success")
    @api.response(400, "Validation Error")
    def get(self, study_id: int, dataset_id: int):  # pylint: disable= unused-argument
        data_obj = model.Dataset.query.get(dataset_id)
        return data_obj.to_dict()

    @api.response(201, "Success")
    @api.response(400, "Validation Error")
    def put(self, study_id: int, dataset_id: int):
        study = model.Study.query.get(study_id)
        if not is_granted("update_dataset", study):
            return "Access denied, you can not modify", 403
        data: typing.Union[dict, typing.Any] = request.json
        data_obj = model.Dataset.query.get(dataset_id)
        data_obj.update(data)
        model.db.session.commit()
        return data_obj.to_dict()

    @api.response(201, "Success")
    @api.response(400, "Validation Error")
    def delete(self, study_id: int, dataset_id: int):
        study = model.Study.query.get(study_id)
        if not is_granted("delete_dataset", study):
            return "Access denied, you can not modify", 403
        data_obj = model.Dataset.query.get(dataset_id)
        for version in data_obj.dataset_versions:
            model.db.session.delete(version)
        model.db.session.delete(data_obj)
        model.db.session.commit()
        dataset_ = study.dataset
        return [d.to_dict() for d in dataset_], 201

    # def delete(self, study_id: int, dataset_id: int, version_id: int):
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
    def get(
        self, study_id: int, dataset_id: int, version_id: int
    ):  # pylint: disable= unused-argument
        dataset_version = model.Version.query.get(version_id)
        return dataset_version.to_dict()

    def put(
        self, study_id: int, dataset_id: int, version_id: int
    ):  # pylint: disable= unused-argument
        study = model.Study.query.get(study_id)
        if not is_granted("publish_dataset", study):
            return "Access denied, you can not modify", 403
        data_version_obj = model.Version.query.get(version_id)
        data_version_obj.update(request.json)
        model.db.session.commit()
        return jsonify(data_version_obj.to_dict()), 201

    def delete(
        self, study_id: int, dataset_id: int, version_id: int
    ):  # pylint: disable= unused-argument
        study = model.Study.query.get(study_id)
        if not is_granted("delete_dataset", study):
            return "Access denied, you can not modify", 403
        data_obj = model.Dataset.query.get(dataset_id)
        for version in data_obj.dataset_versions:
            model.db.session.delete(version)
            model.db.session.commit()
        model.db.session.delete(data_obj)
        model.db.session.commit()
        return Response(status=204)


@api.route("/study/<study_id>/dataset/<dataset_id>/version")
class VersionList(Resource):
    @api.response(201, "Success")
    @api.response(400, "Validation Error")
    @api.doc("versions")
    def get(self, study_id: int, dataset_id: int):
        study = model.Study.query.get(study_id)
        if not is_granted("version", study):
            return "Access denied, you can not modify", 403
        dataset_obj = model.Dataset.query.get(dataset_id)
        return [i.to_dict() for i in dataset_obj.dataset_versions.all()], 200

    @api.response(201, "Success")
    @api.response(400, "Validation Error")
    @api.doc("version add")
    def post(self, study_id: int, dataset_id: int):
        study = model.Study.query.get(study_id)
        if not is_granted("version", study):
            return "Access denied, you can not modify", 403

        data: typing.Union[typing.Any, dict] = request.json
        # data["participants"] = [
        #     model.Participant.query.get(i) for i in data["participants"]
        # ]
        data_obj = model.Dataset.query.get(dataset_id)
        dataset_versions = model.Version.from_data(data_obj, data)
        model.db.session.add(dataset_versions)
        model.db.session.commit()
        return dataset_versions.to_dict()


@api.route("/study/<study_id>/dataset/<dataset_id>/version/<version_id>/publish")
class PublishResource(Resource):
    @api.response(201, "Success")
    @api.response(400, "Validation Error")
    @api.doc("version publish")
    def post(self, study_id: int, dataset_id: int):
        study = model.Study.query.get(study_id)
        if not is_granted("publish_version", study):
            return "Access denied, you can not modify", 403
        data_obj = model.Dataset.query.get(dataset_id)
        data: typing.Union[typing.Any, dict] = request.json
        dataset_versions = model.Version.from_data(data_obj, data)
        model.db.session.commit()
        return dataset_versions.to_dict()
