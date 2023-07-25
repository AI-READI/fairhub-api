import random
from flask import Blueprint, jsonify, request
from model import Study, db, User


study = Blueprint("study", __name__)


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

    studies = Study.query.all()
    return jsonify([s.to_dict() for s in studies])


@study.route("/study/<studyId>", methods=["GET"])
def getStudy(studyId):

    study1 = Study.query.get(studyId)
    return jsonify(study1.to_dict())


@study.route("/study/add", methods=["POST"])
def add_study():
    add_study = Study.from_data(request.json)
    # if not addStudy.validate():
    #     return 'error', 422
    db.session.add(add_study)
    db.session.commit()

    return jsonify(add_study.to_dict()), 201


@study.route("/viewProfile", methods=["POST"])
def update_user_profile():
    data = request.json

    if data is not None:
        data["id"] = 3

    return jsonify(data), 201


@study.route("/study/<studyId>", methods=["POST"])
def update_study(studyId):
    update_study = Study.query.get(studyId)
    # if not addStudy.validate():
    #     return 'error', 422
    update_study.update(request.json)
    db.session.commit()

    return jsonify(update_study.to_dict()), 200
