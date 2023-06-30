from __main__ import app
from flask import request
from flask import jsonify


@app.route("/addStudy", methods=["POST"])
def addStudy():
    data = request.json
    data["id"] = 3
    return jsonify(data), 201


@app.route("/viewProfile", methods=["POST"])
def updateviewProfile():
    data = request.json
    data["id"] = 3
    return jsonify(data), 201


@app.route("/study", methods=["POST"])
def updateStudies():
    data = request.json
    data["id"] = 3
    return jsonify(data), 201


@app.route("/study/<studyId>", methods=["POST"])
def updateStudy(studyId):
    data = request.json
    return jsonify(data), 200


@app.route("/study/<studyId>/dataset", methods=["POST"])
def updateDatesets():
    data = request.json
    data["id"] = 3
    return jsonify(data), 201


@app.route("/study/<studyId>/dataset/<datasetId>", methods=["POST"])
def updateDataset(studyId, datasetId):
    data = request.json
    return jsonify(data), 200


@app.route("/study/<studyId>/dataset/<datasetId>/version", methods=["POST"])
def updateDatesetVersions(studyId, datasetId):
    data = request.json
    data["id"] = 3
    return jsonify(data), 201


@app.route("/study/<studyId>/dataset/<datasetId>/version/<versionId>", methods=["POST"])
def updateDatesetVersion(studyId, datasetId, versionId):
    data = request.json
    data["id"] = 3
    return jsonify(data), 201
