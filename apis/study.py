import random
from flask import jsonify, request, Blueprint

study = Blueprint("study", __name__)
from model import Study


@study.route("/viewProfile", methods=["GET"])
def viewProfile():
    dic = {
        "username": "admin",
        "email": "aydan.gasimova2@gmail.com",
        "fullname": "Aydan Gasimova",
        "image": f" https://api.dicebear.com/5.x/shapes/svg?seed=$"
        f"{str(random.randint(0,1000))}",
        "institution": "CALMI2",
        "location": "San Diego, CA",
        "password": "admin",
        "timezone": "(GMT-11:00) Midway Island",
    }
    return jsonify(dic)


@study.route("/study", methods=["GET"])
def getStudies():
    # return [
    #     {
    #         "id": 1,
    #         "title": "AI-READI",
    #         "contributors": [
    #             {
    #                 "affiliations": ["Manager"],
    #                 "firstname": "Bill",
    #                 "lastname": "Sanders",
    #                 "ORCID": "https://orcid.org/0000-0001-7032-2732",
    #                 "roles": ["editor"],
    #                 "email": "bill.sanders@email.org",
    #                 "status": "invited",
    #             },
    #             {
    #                 "name": "Dolores Chambers",
    #                 "email": "dolores.chambers@email.org",
    #                 "role": "viewer",
    #                 "status": "invited",
    #             },
    #             {
    #                 "name": "Bhavesh Patel",
    #                 "email": "bhavesh.patel@email.org",
    #                 "role": "editor",
    #                 "status": "active",
    #             },
    #         ],
    #         "description": "The AI-READI project seeks to create and share a flagship "
    #         "ethically-sourced dataset of type 2 diabetes.",
    #         "image": "https://fairdataihub.org/images/hero/aireadi-logo.png",
    #         "lastPublished": {
    #             "date": "2023-01-13",
    #             "doi": "10.1234/1234",
    #             "version": "v1.0.0",
    #         },
    #         "lastUpdated": "2023-02-13",
    #         "owner": {
    #             "name": "Sanjay Soundarajan",
    #             "email": "sanjay@email.org",
    #             "ORCID": "https://orcid.org/0000-0002-8032-6398",
    #         },
    #         "size": " 2.8 GB",
    #     },
    #     {
    #         "id": 2,
    #         "title": "Study 2",
    #         "contributors": [
    #             {
    #                 "affiliations": ["Manager"],
    #                 "firstname": "Sanjay",
    #                 "lastname": " Soundarajan",
    #                 "ORCID": "https://orcid.org/0000-0001-7032-2732",
    #                 "roles": ["editor", "owner"],
    #                 "email": "sanjay@email.org",
    #                 "status": "active",
    #             },
    #             {
    #                 "affiliations": ["Manager"],
    #                 "firstname": "Bill",
    #                 "lastname": "Sanders",
    #                 "ORCID": "https://orcid.org/0000-0001-7032-2732",
    #                 "roles": ["editor", "owner"],
    #                 "email": "bill.sanders@email.org",
    #                 "status": "invited",
    #             },
    #             {
    #                 "affiliations": ["Manager"],
    #                 "firstname": "Dolores",
    #                 "lastname": "Chambers",
    #                 "ORCID": "https://orcid.org/0000-0001-7032-2732",
    #                 "roles": ["editor", "owner", "viewer"],
    #                 "email": "dolores.chambers@email.org",
    #                 "status": "invited",
    #             },
    #             {
    #                 "affiliations": ["Manager"],
    #                 "firstname": "Bhavesh",
    #                 "lastname": " Patel",
    #                 "ORCID": "https://orcid.org/0000-0001-7032-2732",
    #                 "roles": ["editor", "owner"],
    #                 "email": "bpatel@email.org",
    #                 "status": "active",
    #             },
    #         ],
    #         "description": "Study 2 description",
    #         "image": f"https://api.dicebear.com/5.x/shapes/svg?seed="
    #         f"{str(random.randint(0, 1000))}",
    #         "lastUpdated": "2023-02-05",
    #         "owner": {
    #             "name": "Sanjay Soundarajan",
    #             "email": "sanjay@email.org",
    #             "ORCID": "https://orcid.org/0000-0002-8032-6398",
    #         },
    #         "size": " 1.2 GB",
    #     },
    # ]
    studies = Study.query.all()
    return jsonify([s.to_dict() for s in studies])


@study.route("/study/<studyId>", methods=["GET"])
def getStudy(studyId):
    # dic = {
    #     1: {
    #         "id": 1,
    #         "title": "AI-READI",
    #         "contributors": [
    #             {
    #                 "affiliations": ["Manager"],
    #                 "firstname": "Sanjay",
    #                 "lastname": " Soundarajan",
    #                 "ORCID": "https://orcid.org/0000-0001-7032-2732",
    #                 "roles": ["editor", "owner"],
    #                 "email": "sanjay@email.org",
    #                 "status": "active",
    #             },
    #             {
    #                 "affiliations": ["Manager"],
    #                 "firstname": "Bill",
    #                 "lastname": "Sanders",
    #                 "ORCID": "https://orcid.org/0000-0001-7032-2732",
    #                 "roles": ["editor", "owner"],
    #                 "email": "bill.sanders@email.org",
    #                 "status": "invited",
    #             },
    #             {
    #                 "affiliations": ["Manager"],
    #                 "firstname": "Dolores",
    #                 "lastname": "Chambers",
    #                 "ORCID": "https://orcid.org/0000-0001-7032-2732",
    #                 "roles": ["editor", "owner", "viewer"],
    #                 "email": "dolores.chambers@email.org",
    #                 "status": "invited",
    #             },
    #             {
    #                 "affiliations": ["Manager"],
    #                 "firstname": "Bhavesh",
    #                 "lastname": " Patel",
    #                 "ORCID": "https://orcid.org/0000-0001-7032-2732",
    #                 "roles": ["editor", "owner"],
    #                 "email": "bpatel@email.org",
    #                 "status": "active",
    #             },
    #         ],
    #         "description": "The AI-READI project seeks to create and share a flagship "
    #         "ethically-sourced dataset of type 2 diabetes.",
    #         "image": "https://fairdataihub.org/images/hero/aireadi-logo.png",
    #         "lastPublished": {
    #             "date": "2023-01-13",
    #             "doi": "10.1234/1234",
    #             "version": "v1.0.0",
    #         },
    #         "lastUpdated": "2023-02-13",
    #         "owner": {
    #             "name": "Sanjay Soundarajan",
    #             "email": "sanjay@email.org",
    #             "ORCID": "https://orcid.org/0000-0002-8032-6398",
    #         },
    #         "size": " 2.8 GB",
    #     },
    #     2: {
    #         "id": 2,
    #         "title": "Study 2",
    #         "contributors": [
    #             {
    #                 "affiliations": ["Manager"],
    #                 "firstname": "Sanjay",
    #                 "lastname": " Soundarajan",
    #                 "ORCID": "https://orcid.org/0000-0001-7032-2732",
    #                 "roles": ["editor", "owner"],
    #                 "email": "sanjay@email.org",
    #                 "status": "active",
    #             },
    #             {
    #                 "affiliations": ["Manager"],
    #                 "firstname": "Bill",
    #                 "lastname": "Sanders",
    #                 "ORCID": "https://orcid.org/0000-0001-7032-2732",
    #                 "roles": ["editor", "owner"],
    #                 "email": "bill.sanders@email.org",
    #                 "status": "invited",
    #             },
    #             {
    #                 "affiliations": ["Manager"],
    #                 "firstname": "Dolores",
    #                 "lastname": "Chambers",
    #                 "ORCID": "https://orcid.org/0000-0001-7032-2732",
    #                 "roles": ["editor", "owner", "viewer"],
    #                 "email": "dolores.chambers@email.org",
    #                 "status": "invited",
    #             },
    #             {
    #                 "affiliations": ["Manager"],
    #                 "firstname": "Bhavesh",
    #                 "lastname": " Patel",
    #                 "ORCID": "https://orcid.org/0000-0001-7032-2732",
    #                 "roles": ["editor", "owner"],
    #                 "email": "bpatel@email.org",
    #                 "status": "active",
    #             },
    #         ],
    #         "description": "Study 2 description",
    #         "image": f"https://api.dicebear.com/5.x/shapes/svg?seed="
    #         f"{str(random.randint(0, 1000))}",
    #         "lastUpdated": "2023-02-05",
    #         "owner": {
    #             "name": "Sanjay Soundarajan",
    #             "email": "sanjay@email.org",
    #             "ORCID": "https://orcid.org/0000-0002-8032-6398",
    #         },
    #         "size": " 1.2 GB",
    #     },
    # }
    # if int(studyId) not in dic:
    #     return "not found", 404
    # jsonify(dic[int(studyId)])

    study1 = Study.query.get(studyId)
    return jsonify(study1.to_dict())


@study.route("/study/add", methods=["POST"])
def add_study():
    data = request.json

    if data is not None:
        data["id"] = 3

    return jsonify(data), 201


@study.route("/viewProfile", methods=["POST"])
def update_view_profile():
    data = request.json

    if data is not None:
        data["id"] = 3

    return jsonify(data), 201


@study.route("/study", methods=["POST"])
def update_studies():
    data = request.json

    if data is not None:
        data["id"] = 3

    return jsonify(data), 201


@study.route("/study/<studyId>", methods=["POST"])
def update_study(studyId):
    data = request.json
    return jsonify(data), 200
