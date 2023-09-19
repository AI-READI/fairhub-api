from flask_restx import Namespace, Resource, fields

from model import StudyContributor, Study, db

api = Namespace("Contributor", description="Contributors", path="/")


contributors_model = api.model(
    "Version",
    {
        "user_id": fields.String(required=True),
        "permission": fields.String(required=True),
        "study_id": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/contributor")
class AddParticipant(Resource):
    @api.doc("contributor list")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(contributors_model)
    def get(self, study_id: int):
        contributors = StudyContributor.query.all()
        return [c.to_dict() for c in contributors]

    def put(self, study_id: int):
        contributors = StudyContributor.query.all()

    def delete(self, study_id: int):
        study = Study.query.get(study_id)
        contributors = Study.query.filter_by(contributors=study.study_contributors.user_id)
        db.session.delete(contributors)
