import random
from __main__ import app
from flask import jsonify


@app.route('/study', methods=['GET'])
def getStudies():
    return [{
        'id': 1,
        'title': 'AI-READI',
        "contributors": [
            {
                "name": "Bill Sanders",
                "email": "bill.sanders@email.org",
                "role": "editor",
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
        "description": 'The AI-READI project seeks to create and share a flagship '
                        'ethically-sourced dataset of type 2 diabetes.',
        "image": 'https://fairdataihub.org/images/hero/aireadi-logo.png',
        "lastPublished": {
            "date": "2023-01-13",
            "doi": "10.1234/1234",
            "version": "v1.0.0"
        },
        "lastUpdated": "2023-02-13",
        "owner": {
            "name": "Sanjay Soundarajan",
            "email": "sanjay@email.org",
        },
        "size": " 2.8 GB"
    },
        {
            'id': 2,
            "title": 'Study 2',
            "contributors": [
                {
                    "name": "Sanjay Soundarajan",
                    "email": "sanjay@email.org",
                    "role": "owner",
                    "status": "active",
                },
                {
                    "name": "Bill Sanders",
                    "email": "bill.sanders@email.org",
                    "role": "editor",
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
            "description": 'Study 2 description',
            "image": f'https://api.dicebear.com/5.x/shapes/svg?seed={str(random.randint(0, 1000))}',
            "lastUpdated": "2023-02-05",
            "owner": {"name": 'Sanjay Soundarajan',
                      "email": "sanjay@email.org"},
            "size": " 1.2 GB",
         },
    ]


@app.route('/study/<studyId>', methods=['GET'])
def getStudy(studyId):

    dic = {1:  {
        "id": 1,
        "contributors": [
            {
                "affiliations": ["Manager"],
                "firstname": "Bhavesh",
                "lastname": "Patel",
                "ORCID": "https://orcid.org/0000-0001-7032-2732",
                "roles": ["Developer"]
            }
        ],
        "title": "aireadi",
        "description": "AI model",
        "keywords": ['AI model'],
        "primaryLanguage": "english",
        "selectedParticipants": []
    }, 2:  {
        "id": 2,
        "contributors": [
            {
                "affiliations": ["Manager"],
                "firstname": "Sanjay",
                "lastname": "Soundarajan",
                "ORCID": "https://orcid.org/0000-0101-111-2732",
                "roles": ["Developer"]
            }
        ],
        "title": "study 2",
        "description": "AI model",
        "keywords": ['AI model'],
        "primaryLanguage": "english",
        "selectedParticipants": []
    }}
    if int(studyId) not in dic:
        return 'not found', 404
    return jsonify(dic[int(studyId)])


@app.route('/study/<studyId>/dataset', methods=['GET'])
def getDatasets(studyId):
    datasets = {
        1:
       [
           {
            "id": 1,
            "name": 'AI-READI',
            "versions": [{'id':1},{'id':2}]
        },
        {
            "id": 2,
            "name": 'AI-READI2',
            "versions": [{'id': 1},{'id':2}]
        }],
        2:
       [
           {
            "id": 1,
            "name": 'AI-READI3',
            "versions": [{'id': 1}, {'id': 2}]
        },
        {
            "id": 2,
            "name": 'AI-READI4'
        }]
    }

    if int(studyId) not in datasets:
        return 'not found', 404
    return jsonify(datasets[int(studyId)])


@app.route("/study/<studyId>/dataset/<datasetId>/version/<versionId>", methods=['GET'])
def getDatasetVersion(studyId,datasetId, versionId):
    dic = {
        1: {
            "id": 1,
            "contributors": [
                {
                    "affiliations": ["Manager"],
                    "firstname": "Bhavesh",
                    "lastname": "Patel",
                    "ORCID": "https://orcid.org/0000-0001-7032-2732",
                    "roles": ["Developer"]
                }
            ],
            "title": "AI-READI",
            "description": "AI model",
            "keywords": ['AI model'],
            "primaryLanguage": "english",
            "selectedParticipants": []},
        2: {
            "id": 2,
            "contributors": [
                {
                    "affiliations": ["Manager"],
                    "firstname": "Bhavesh",
                    "lastname": "Patel",
                    "ORCID": "https://orcid.org/0000-0001-7032-2732",
                    "roles": ["Developer"]
                }
            ],
            "title": "AI-READI",
            "description": "AI model",
            "keywords": ['AI model'],
            "primaryLanguage": "english",
            "selectedParticipants": []
        },
    }
    if int(studyId) not in dic:
        return 'not found', 404
    return jsonify(dic[int(studyId)])

