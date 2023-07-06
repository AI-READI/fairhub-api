import random
from flask import jsonify, request, Blueprint
from faker import Faker

participant = Blueprint("participant", __name__)

@participant.route("/study/<studyId>/participants", methods=["GET"])
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


@participant.route("/study/<studyId>/participants/add", methods=["POST"])
def add_participants(studyId):
    data = request.json
    return jsonify(data)