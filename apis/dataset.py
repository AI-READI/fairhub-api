from flask import Blueprint, jsonify, request, Response

from model import Dataset, DatasetVersion, db, Study, Participant

dataset = Blueprint("dataset", __name__)


@dataset.route("/study/<studyId>/dataset", methods=["GET"])
def getDatasets(studyId):
    study = Study.query.get(studyId)
    datasets = Dataset.query.filter_by(study=study)
    return jsonify([d.to_dict() for d in datasets])


@dataset.route(
    "/study/<studyId>/dataset/<datasetId>/version/<versionId>", methods=["GET"]
)
def getDatasetVersion(studyId, datasetId, versionId):
    # if int(studyId) not in dic:
    #     return "not found", 404
    dataset_version = DatasetVersion.query.get(versionId)
    return jsonify(dataset_version.to_dict())


@dataset.route("/study/<studyId>/dataset", methods=["POST"])
def add_datasets(studyId):
    study = Study.query.get(studyId)
    dataset_obj = Dataset(study)
    dataset_version = DatasetVersion.from_data(dataset_obj, request.json)
    db.session.add(dataset_obj)
    db.session.add(dataset_version)
    db.session.commit()
    return jsonify(dataset_version.to_dict()), 201


@dataset.route("/study/<studyId>/dataset/<datasetId>", methods=["POST"])
def update_dataset(studyId, datasetId):
    pass


@dataset.route("/study/<studyId>/dataset/<datasetId>/version", methods=["POST"])
def add_dataset_version(studyId, datasetId):
    data = request.json
    data["participants"] = [Participant.query.get(i) for i in data["participants"]]
    data_obj = Dataset.query.get(datasetId)
    dataset_version = DatasetVersion.from_data(data, data_obj)
    db.session.add(dataset_version)
    db.session.commit()

    return jsonify(dataset_version.to_dict()), 201


@dataset.route(
    "/study/<studyId>/dataset/<datasetId>/version/<versionId>", methods=["PUT"]
)
def modify_dateset_version(studyId, datasetId, versionId):
    data_version_obj = DatasetVersion.query.get(versionId)
    data_version_obj.update(request.json)
    db.session.commit()
    return jsonify(data_version_obj.to_dict()), 200


@dataset.route(
    "/study/<studyId>/dataset/<datasetId>/version/<versionId>", methods=["DELETE"]
)
def delete_dateset_version(studyId, datasetId, versionId):
    data_obj = Dataset.query.get(datasetId)
    for version in data_obj.dataset_versions:
        db.session.delete(version)
        db.session.commit()
    db.session.delete(data_obj)
    db.session.commit()
    return Response(status=204)
