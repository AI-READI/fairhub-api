from flask import Blueprint, jsonify, request, Response

from model import Dataset, DatasetVersion, db, Study, Participant

dataset = Blueprint("dataset", __name__)


# @dataset.route("/study/<study_id>/dataset", methods=["GET"])
# def getDatasets(study_id):
#     study = Study.query.get(study_id)
#     datasets = Dataset.query.filter_by(study=study)
#     return jsonify([d.to_dict() for d in datasets])


# @dataset.route("/study/<study_id>/dataset/<dataset_id>/version/<version_id>", methods=["GET"])
# def getDatasetVersion(study_id, dataset_id, version_id):
#     # if int(study_id) not in dic:
#     #     return "not found", 404
#     dataset_version = DatasetVersion.query.get(version_id)
#     return jsonify(dataset_version.to_dict())


# @dataset.route("/study/<study_id>/dataset", methods=["POST"])
# def add_datasets(study_id):
#     study = Study.query.get(study_id)
#     dataset_obj = Dataset(study)
#     dataset_version = DatasetVersion.from_data(dataset_obj, request.json)
#     db.session.add(dataset_obj)
#     db.session.add(dataset_version)
#     db.session.commit()
#     return jsonify(dataset_version.to_dict()), 201
#

@dataset.route("/study/<study_id>/dataset/<dataset_id>", methods=["POST"])
def update_dataset(study_id, dataset_id):
    pass


@dataset.route("/study/<study_id>/dataset/<dataset_id>/version", methods=["POST"])
def add_dataset_version(study_id, dataset_id):
    data = request.json
    data["participants"] = [Participant.query.get(i) for i in data["participants"]]
    data_obj = Dataset.query.get(dataset_id)
    dataset_version = DatasetVersion.from_data(data, data_obj)
    db.session.add(dataset_version)
    db.session.commit()

    return jsonify(dataset_version.to_dict()), 201


# @dataset.route( "/study/<study_id>/dataset/<dataset_id>/version/<version_id>", methods=["PUT"]
# )
# def modify_dateset_version(study_i_id, dataset_id, version_id):
#     data_version_obj = DatasetVersion.query.get(version_id)
#     data_version_obj.update(request.json)
#     db.session.commit()
#     return jsonify(data_version_obj.to_dict()), 200
#
#
# @dataset.route( "/study/<study_id>/dataset/<dataset_id>/version/<version_id>", methods=["DELETE"])
# def delete_dateset_version(study_id, dataset_id, versionId):
#     data_obj = Dataset.query.get(dataset_id)
#     for version in data_obj.dataset_versions:
#         db.session.delete(version)
#         db.session.commit()
#     db.session.delete(data_obj)
#     db.session.commit()
#     return Response(status=204)

