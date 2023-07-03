from flask import jsonify, request
from __main__ import app


@app.route("/addStudy", methods=["POST"])
def add_study():
    data = request.json

    if data is not None:
        data["id"] = 3

    return jsonify(data), 201


@app.route("/viewProfile", methods=["POST"])
def update_view_profile():
    data = request.json

    if data is not None:
        data["id"] = 3

    return jsonify(data), 201


@app.route("/study", methods=["POST"])
def update_studies():
    data = request.json

    if data is not None:
        data["id"] = 3

    return jsonify(data), 201


@app.route("/study/<studyId>", methods=["POST"])
def update_study(studyId):
    data = request.json
    return jsonify(data), 200


@app.route("/study/<studyId>/dataset", methods=["POST"])
def update_datesets():
    data = request.json

    if data is not None:
        data["id"] = 3

    return jsonify(data), 201


@app.route("/study/<studyId>/dataset/<datasetId>", methods=["POST"])
def update_dataset(studyId, datasetId):
    data = request.json

    return jsonify(data), 200


@app.route("/study/<studyId>/dataset/<datasetId>/version", methods=["POST"])
def update_dateset_versions(studyId, datasetId):
    data = request.json

    if data is not None:
        data["id"] = 3

    return jsonify(data), 201


@app.route("/study/<studyId>/dataset/<datasetId>/version/<versionId>", methods=["POST"])
def update_dateset_version(studyId, datasetId, versionId):
    data = request.json

    if data is not None:
        data["id"] = 3

    return jsonify(data), 201


@app.route("/study/<studyId>/participants/add", methods=["POST"])
def add_participants(studyId):
    data = request.json
    return jsonify(data)
