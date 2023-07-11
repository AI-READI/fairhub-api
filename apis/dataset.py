from flask import request, Blueprint
import random
from flask import jsonify
from faker import Faker
from model import Dataset
from model import DatasetVersions
dataset = Blueprint("dataset", __name__)


@dataset.route("/study/<studyId>/dataset", methods=["GET"])
def getDatasets(studyId):
    # datasets = {
    #     1: [
    #         {
    #             "id": 1,
    #             "name": "AI-READI",
    #             "publishedVersion": 1,
    #             "latestVersion": 2,
    #             "lastModified": "2023-03-21",
    #             "lastPublished": "2023-01-20",
    #         },
    #         {
    #             "id": 2,
    #             "name": "AI-READI2",
    #             "publishedVersion": 2,
    #             "latestVersion": 2,
    #             "lastModified": "2023-01-20",
    #             "lastPublished": "2023-01-20",
    #         },
    #     ],
    #     2: [
    #         {
    #             "id": 1,
    #             "name": "AI-READI3",
    #             "publishedVersion": 2,
    #             "latestVersion": 2,
    #             "lastModified": "2023-01-20",
    #             "lastPublished": "2023-01-20",
    #         },
    #         {
    #             "id": 2,
    #             "name": "AI-READI4",
    #             "publishedVersion": 2,
    #             "latestVersion": 2,
    #             "lastModified": "2023-01-20",
    #             "lastPublished": "2023-01-20",
    #         },
    #     ],
    # }
    #
    # if int(studyId) not in datasets:
    #     return "not found", 404
    # return jsonify(datasets[int(studyId)])
    datasets = Dataset.query.all()
    return jsonify([d.to_dict() for d in datasets])


@dataset.route("/study/<studyId>/dataset/<datasetId>/version/<versionId>", methods=["GET"])
def getDatasetVersion(studyId, datasetId, versionId):
    # dic = {
    #     # Study 1
    #     1: {
    #         # Dataset 1
    #         1: {
    #             # Version 1
    #             1: {
    #                 "id": 1,
    #                 "contributors": [
    #                     {
    #                         "affiliations": ["Manager"],
    #                         "firstname": "Dolores",
    #                         "lastname": "Chambers",
    #                         "ORCID": "https://orcid.org/0000-0001-7032-2732",
    #                         "roles": ["editor", "owner", "viewer"],
    #                         "email": "dolores.chambers@email.org",
    #                         "status": "invited",
    #                     },
    #                     {
    #                         "affiliations": ["Manager"],
    #                         "firstname": "Bhavesh",
    #                         "lastname": " Patel",
    #                         "ORCID": "https://orcid.org/0000-0001-7032-2732",
    #                         "roles": ["editor", "owner"],
    #                         "email": "bpatel@email.org",
    #                         "status": "active",
    #                     },
    #                 ],
    #                 "title": "AI-READI",
    #                 "description": "AI model for diabetics",
    #                 "keywords": ["AI model"],
    #                 "primaryLanguage": "english",
    #                 "selectedParticipants": [],
    #                 "published": True,
    #             },
    #             # Version 2
    #             2: {
    #                 "id": 2,
    #                 "contributors": [
    #                     {
    #                         "affiliations": ["Manager"],
    #                         "firstname": "Dolores",
    #                         "lastname": "Chambers",
    #                         "ORCID": "https://orcid.org/0000-0001-7032-2732",
    #                         "roles": ["editor", "owner", "viewer"],
    #                         "email": "dolores.chambers@email.org",
    #                         "status": "invited",
    #                     },
    #                     {
    #                         "affiliations": ["Manager"],
    #                         "firstname": "Bhavesh",
    #                         "lastname": " Patel",
    #                         "ORCID": "https://orcid.org/0000-0001-7032-2732",
    #                         "roles": ["editor", "owner"],
    #                         "email": "bpatel@email.org",
    #                         "status": "active",
    #                     },
    #                 ],
    #                 "title": "AI-READI",
    #                 "description": "AI model for diabetics",
    #                 "keywords": ["AI model"],
    #                 "primaryLanguage": "english",
    #                 "selectedParticipants": [],
    #                 "published": False,
    #             },
    #         },
    #         # Dataset 2
    #         2: {
    #             # Version 2
    #             2: {
    #                 "id": 2,
    #                 "contributors": [
    #                     {
    #                         "affiliations": ["Manager"],
    #                         "firstname": "Bhavesh",
    #                         "lastname": "Patel",
    #                         "ORCID": "https://orcid.org/0000-0001-7032-2732",
    #                         "roles": ["Developer"],
    #                         "email": "bpatel@calmi2.org",
    #                         "status": "invited",
    #                     }
    #                 ],
    #                 "title": "AI-READI",
    #                 "description": "AI model for diabetics",
    #                 "keywords": ["AI model"],
    #                 "primaryLanguage": "english",
    #                 "selectedParticipants": [],
    #                 "published": True,
    #             }
    #         },
    #     },
    #     # Study 2
    #     2: {
    #         # Dataset 1
    #         1: {
    #             # Version 2
    #             2: {
    #                 "id": 2,
    #                 "contributors": [
    #                     {
    #                         "affiliations": ["Manager"],
    #                         "firstname": "Bhavesh",
    #                         "lastname": "Patel",
    #                         "ORCID": "https://orcid.org/0000-0001-7032-2732",
    #                         "roles": ["Developer"],
    #                         "email": "bpatel@calmi2.org",
    #                         "status": "invited",
    #                     }
    #                 ],
    #                 "title": "AI-READI",
    #                 "description": "AI model",
    #                 "keywords": ["AI model", "diabetics"],
    #                 "primaryLanguage": "english",
    #                 "selectedParticipants": [],
    #                 "published": True,
    #             }
    #         },
    #         # Dataset 2
    #         2: {
    #             # Version 2
    #             2: {
    #                 "id": 2,
    #                 "contributors": [
    #                     {
    #                         "affiliations": ["Manager"],
    #                         "firstname": "Bhavesh",
    #                         "lastname": "Patel",
    #                         "ORCID": "https://orcid.org/0000-0001-7032-2732",
    #                         "roles": ["Developer"],
    #                         "email": "bpatel@calmi2.org",
    #                         "status": "invited",
    #                     }
    #                 ],
    #                 "title": "AI-READI",
    #                 "description": "AI model",
    #                 "keywords": ["diabetics"],
    #                 "primaryLanguage": "english",
    #                 "selectedParticipants": [],
    #                 "published": True,
    #             }
    #         },
    #     },
    # }
    # if int(studyId) not in dic:
    #     return "not found", 404
    # return jsonify(dic[int(studyId)][int(datasetId)][int(versionId)])
    pass
    lastPublished= DatasetVersions.query.order_by('lastPublished').limit(1)
    lastModified= DatasetVersions.query.order_by('lastModified').limit(1)


@dataset.route("/study/<studyId>/dataset/<datasetId>", methods=["POST"])
def update_dataset(studyId, datasetId):
    data = request.json

    return jsonify(data), 200


@dataset.route("/study/<studyId>/dataset", methods=["POST"])
def update_datesets():
    data = request.json

    if data is not None:
        data["id"] = 3

    return jsonify(data), 201


@dataset.route("/study/<studyId>/dataset/<datasetId>/version", methods=["POST"])
def update_dateset_versions(studyId, datasetId):
    data = request.json

    if data is not None:
        data["id"] = 3

    return jsonify(data), 201


@dataset.route("/study/<studyId>/dataset/<datasetId>/version/<versionId>", methods=["POST"])
def update_dateset_version(studyId, datasetId, versionId):
    data = request.json

    if data is not None:
        data["id"] = 3

    return jsonify(data), 201
