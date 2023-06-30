from __main__ import app
from faker import Faker
from flask import jsonify, request


@app.route("/study/<studyId>/participants", methods=["GET"])
def get_participants(studyId):
    fake = Faker()
    data = [
        {
            "participant_id": _ + 1,
            "name": fake.name(),
            "address": fake.street_address(),
            "age": fake.random_int(min=1, max=99),
        }
        for _ in range(30)
    ]

    return data


@app.route("/study/<studyId>/participants/add", methods=["POST"])
def add_participants(studyId):
    data = request.json
    return jsonify(data)
