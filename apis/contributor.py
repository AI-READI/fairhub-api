from flask import Blueprint, jsonify, request
from model import db, User

contributor = Blueprint("contributor", __name__)


@contributor.route("/study/<study_id>/contributor", methods=["GET"])
def get_participants(study_id):
    contributors = User.query.all()
    return jsonify([c.to_dict() for c in contributors])


# in progress update participants


@contributor.route("/study/<study_id>/contributor/<contributor_id>", methods=["DELETE"])
def update_participants(study_id, contributor_id):
    contributors = User.query.get(contributor_id)
    contributors.update(request.json)
    db.session.delete(contributors)
    db.session.commit()
