from flask import Blueprint, jsonify, request
from model import db, User

contributor = Blueprint("contributor", __name__)


@contributor.route("/study/<studyId>/contributor", methods=["GET"])
def get_participants(studyId):

    contributors = User.query.all()
    return jsonify([c.to_dict() for c in contributors])


# in progress update participants
@contributor.route("/study/<studyId>/contributor/<contributor_id>", methods=["POST"])
def update_participants(studyId, contributor_id):
    update_contributor = User.query.get(contributor_id)
    update_contributor.update(request.json)
    db.session.commit()
    return jsonify(update_contributor.to_dict()), 200
