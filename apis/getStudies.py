import random

from __main__ import app
from flask import jsonify


@app.route("/study", methods=["GET"])
def getStudies():
    return [
        {
            "id": 1,
            "title": "AI-READI",
            "contributors": [
                {
                    "affiliations": ["Manager"],
                    "firstname": "Bill",
                    "lastname": "Sanders",
                    "ORCID": "https://orcid.org/0000-0001-7032-2732",
                    "roles": ["editor"],
                    "email": "bill.sanders@email.org",
                    "status": "invited",
                },
                {
                    "name": "Dolores Chambers",
                    "email": "dolores.chambers@email.org",
                    "role": "viewer",
                    "status": "invited",
                },
                {
                    "name": "Bhavesh Patel",
                    "email": "bhavesh.patel@email.org",
                    "role": "editor",
                    "status": "active",
                },
            ],
            "description": "The AI-READI project seeks to create and share a flagship "
            "ethically-sourced dataset of type 2 diabetes.",
            "image": "https://fairdataihub.org/images/hero/aireadi-logo.png",
            "lastPublished": {
                "date": "2023-01-13",
                "doi": "10.1234/1234",
                "version": "v1.0.0",
            },
            "lastUpdated": "2023-02-13",
            "owner": {
                "name": "Sanjay Soundarajan",
                "email": "sanjay@email.org",
                "ORCID": "https://orcid.org/0000-0002-8032-6398",
            },
            "size": " 2.8 GB",
        },
        {
            "id": 2,
            "title": "Study 2",
            "contributors": [
                {
                    "affiliations": ["Manager"],
                    "firstname": "Sanjay",
                    "lastname": " Soundarajan",
                    "ORCID": "https://orcid.org/0000-0001-7032-2732",
                    "roles": ["editor", "owner"],
                    "email": "sanjay@email.org",
                    "status": "active",
                },
                {
                    "affiliations": ["Manager"],
                    "firstname": "Bill",
                    "lastname": "Sanders",
                    "ORCID": "https://orcid.org/0000-0001-7032-2732",
                    "roles": ["editor", "owner"],
                    "email": "bill.sanders@email.org",
                    "status": "invited",
                },
                {
                    "affiliations": ["Manager"],
                    "firstname": "Dolores",
                    "lastname": "Chambers",
                    "ORCID": "https://orcid.org/0000-0001-7032-2732",
                    "roles": ["editor", "owner", "viewer"],
                    "email": "dolores.chambers@email.org",
                    "status": "invited",
                },
                {
                    "affiliations": ["Manager"],
                    "firstname": "Bhavesh",
                    "lastname": " Patel",
                    "ORCID": "https://orcid.org/0000-0001-7032-2732",
                    "roles": ["editor", "owner"],
                    "email": "bpatel@email.org",
                    "status": "active",
                },
            ],
            "description": "Study 2 description",
            "image": f"https://api.dicebear.com/5.x/shapes/svg?seed="
            f"{str(random.randint(0, 1000))}",
            "lastUpdated": "2023-02-05",
            "owner": {
                "name": "Sanjay Soundarajan",
                "email": "sanjay@email.org",
                "ORCID": "https://orcid.org/0000-0002-8032-6398",
            },
            "size": " 1.2 GB",
        },
    ]


@app.route("/study/<studyId>", methods=["GET"])
def getStudy(studyId):
    dic = {
        1: {
            "id": 1,
            "title": "AI-READI",
            "contributors": [
                {
                    "affiliations": ["Manager"],
                    "firstname": "Sanjay",
                    "lastname": " Soundarajan",
                    "ORCID": "https://orcid.org/0000-0001-7032-2732",
                    "roles": ["editor", "owner"],
                    "email": "sanjay@email.org",
                    "status": "active",
                },
                {
                    "affiliations": ["Manager"],
                    "firstname": "Bill",
                    "lastname": "Sanders",
                    "ORCID": "https://orcid.org/0000-0001-7032-2732",
                    "roles": ["editor", "owner"],
                    "email": "bill.sanders@email.org",
                    "status": "invited",
                },
                {
                    "affiliations": ["Manager"],
                    "firstname": "Dolores",
                    "lastname": "Chambers",
                    "ORCID": "https://orcid.org/0000-0001-7032-2732",
                    "roles": ["editor", "owner", "viewer"],
                    "email": "dolores.chambers@email.org",
                    "status": "invited",
                },
                {
                    "affiliations": ["Manager"],
                    "firstname": "Bhavesh",
                    "lastname": " Patel",
                    "ORCID": "https://orcid.org/0000-0001-7032-2732",
                    "roles": ["editor", "owner"],
                    "email": "bpatel@email.org",
                    "status": "active",
                },
            ],
            "description": "The AI-READI project seeks to create and share a flagship "
            "ethically-sourced dataset of type 2 diabetes.",
            "image": "https://fairdataihub.org/images/hero/aireadi-logo.png",
            "lastPublished": {
                "date": "2023-01-13",
                "doi": "10.1234/1234",
                "version": "v1.0.0",
            },
            "lastUpdated": "2023-02-13",
            "owner": {
                "name": "Sanjay Soundarajan",
                "email": "sanjay@email.org",
                "ORCID": "https://orcid.org/0000-0002-8032-6398",
            },
            "size": " 2.8 GB",
        },
        2: {
            "id": 2,
            "title": "Study 2",
            "contributors": [
                {
                    "affiliations": ["Manager"],
                    "firstname": "Sanjay",
                    "lastname": " Soundarajan",
                    "ORCID": "https://orcid.org/0000-0001-7032-2732",
                    "roles": ["editor", "owner"],
                    "email": "sanjay@email.org",
                    "status": "active",
                },
                {
                    "affiliations": ["Manager"],
                    "firstname": "Bill",
                    "lastname": "Sanders",
                    "ORCID": "https://orcid.org/0000-0001-7032-2732",
                    "roles": ["editor", "owner"],
                    "email": "bill.sanders@email.org",
                    "status": "invited",
                },
                {
                    "affiliations": ["Manager"],
                    "firstname": "Dolores",
                    "lastname": "Chambers",
                    "ORCID": "https://orcid.org/0000-0001-7032-2732",
                    "roles": ["editor", "owner", "viewer"],
                    "email": "dolores.chambers@email.org",
                    "status": "invited",
                },
                {
                    "affiliations": ["Manager"],
                    "firstname": "Bhavesh",
                    "lastname": " Patel",
                    "ORCID": "https://orcid.org/0000-0001-7032-2732",
                    "roles": ["editor", "owner"],
                    "email": "bpatel@email.org",
                    "status": "active",
                },
            ],
            "description": "Study 2 description",
            "image": f"https://api.dicebear.com/5.x/shapes/svg?seed="
            f"{str(random.randint(0, 1000))}",
            "lastUpdated": "2023-02-05",
            "owner": {
                "name": "Sanjay Soundarajan",
                "email": "sanjay@email.org",
                "ORCID": "https://orcid.org/0000-0002-8032-6398",
            },
            "size": " 1.2 GB",
        },
    }
    if int(studyId) not in dic:
        return "not found", 404
    return jsonify(dic[int(studyId)])


@app.route("/study/<studyId>/dataset", methods=["GET"])
def getDatasets(studyId):
    datasets = {
        1: [
            {
                "id": 1,
                "name": "AI-READI",
                "publishedVersion": 1,
                "latestVersion": 2,
                "lastModified": "2023-03-21",
                "lastPublished": "2023-01-20",
            },
            {
                "id": 2,
                "name": "AI-READI2",
                "publishedVersion": 2,
                "latestVersion": 2,
                "lastModified": "2023-01-20",
                "lastPublished": "2023-01-20",
            },
        ],
        2: [
            {
                "id": 1,
                "name": "AI-READI3",
                "publishedVersion": 2,
                "latestVersion": 2,
                "lastModified": "2023-01-20",
                "lastPublished": "2023-01-20",
            },
            {
                "id": 2,
                "name": "AI-READI4",
                "publishedVersion": 2,
                "latestVersion": 2,
                "lastModified": "2023-01-20",
                "lastPublished": "2023-01-20",
            },
        ],
    }

    if int(studyId) not in datasets:
        return "not found", 404
    return jsonify(datasets[int(studyId)])


@app.route("/study/<studyId>/dataset/<datasetId>/version/<versionId>", methods=["GET"])
def getDatasetVersion(studyId, datasetId, versionId):
    dic = {
        # Study 1
        1: {
            # Dataset 1
            1: {
                # Version 1
                1: {
                    "id": 1,
                    "contributors": [
                        {
                            "affiliations": ["Manager"],
                            "firstname": "Dolores",
                            "lastname": "Chambers",
                            "ORCID": "https://orcid.org/0000-0001-7032-2732",
                            "roles": ["editor", "owner", "viewer"],
                            "email": "dolores.chambers@email.org",
                            "status": "invited",
                        },
                        {
                            "affiliations": ["Manager"],
                            "firstname": "Bhavesh",
                            "lastname": " Patel",
                            "ORCID": "https://orcid.org/0000-0001-7032-2732",
                            "roles": ["editor", "owner"],
                            "email": "bpatel@email.org",
                            "status": "active",
                        },
                    ],
                    "title": "AI-READI",
                    "description": "AI model for diabetics",
                    "keywords": ["AI model"],
                    "primaryLanguage": "english",
                    "selectedParticipants": [],
                    "published": True,
                },
                # Version 2
                2: {
                    "id": 2,
                    "contributors": [
                        {
                            "affiliations": ["Manager"],
                            "firstname": "Dolores",
                            "lastname": "Chambers",
                            "ORCID": "https://orcid.org/0000-0001-7032-2732",
                            "roles": ["editor", "owner", "viewer"],
                            "email": "dolores.chambers@email.org",
                            "status": "invited",
                        },
                        {
                            "affiliations": ["Manager"],
                            "firstname": "Bhavesh",
                            "lastname": " Patel",
                            "ORCID": "https://orcid.org/0000-0001-7032-2732",
                            "roles": ["editor", "owner"],
                            "email": "bpatel@email.org",
                            "status": "active",
                        },
                    ],
                    "title": "AI-READI",
                    "description": "AI model for diabetics",
                    "keywords": ["AI model"],
                    "primaryLanguage": "english",
                    "selectedParticipants": [],
                    "published": False,
                },
            },
            # Dataset 2
            2: {
                # Version 2
                2: {
                    "id": 2,
                    "contributors": [
                        {
                            "affiliations": ["Manager"],
                            "firstname": "Bhavesh",
                            "lastname": "Patel",
                            "ORCID": "https://orcid.org/0000-0001-7032-2732",
                            "roles": ["Developer"],
                            "email": "bpatel@calmi2.org",
                            "status": "invited",
                        }
                    ],
                    "title": "AI-READI",
                    "description": "AI model for diabetics",
                    "keywords": ["AI model"],
                    "primaryLanguage": "english",
                    "selectedParticipants": [],
                    "published": True,
                }
            },
        },
        # Study 2
        2: {
            # Dataset 1
            1: {
                # Version 2
                2: {
                    "id": 2,
                    "contributors": [
                        {
                            "affiliations": ["Manager"],
                            "firstname": "Bhavesh",
                            "lastname": "Patel",
                            "ORCID": "https://orcid.org/0000-0001-7032-2732",
                            "roles": ["Developer"],
                            "email": "bpatel@calmi2.org",
                            "status": "invited",
                        }
                    ],
                    "title": "AI-READI",
                    "description": "AI model",
                    "keywords": ["AI model", "diabetics"],
                    "primaryLanguage": "english",
                    "selectedParticipants": [],
                    "published": True,
                }
            },
            # Dataset 2
            2: {
                # Version 2
                2: {
                    "id": 2,
                    "contributors": [
                        {
                            "affiliations": ["Manager"],
                            "firstname": "Bhavesh",
                            "lastname": "Patel",
                            "ORCID": "https://orcid.org/0000-0001-7032-2732",
                            "roles": ["Developer"],
                            "email": "bpatel@calmi2.org",
                            "status": "invited",
                        }
                    ],
                    "title": "AI-READI",
                    "description": "AI model",
                    "keywords": ["diabetics"],
                    "primaryLanguage": "english",
                    "selectedParticipants": [],
                    "published": True,
                }
            },
        },
    }
    if int(studyId) not in dic:
        return "not found", 404
    return jsonify(dic[int(studyId)][int(datasetId)][int(versionId)])


@app.route("/viewProfile", methods=["GET"])
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
