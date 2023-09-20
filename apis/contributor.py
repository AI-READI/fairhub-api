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
class AddContributor(Resource):
    @api.doc("contributor list")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(contributors_model)
    def get(self, study_id: int):
        contributors = StudyContributor.query.all()
        return [c.to_dict() for c in contributors]

    def put(self, study_id: int):
        contributors = StudyContributor.query.all()


@api.route("/study/<study_id>/contributor/<user_id>")
class DeleteContributor(Resource):
    @api.doc("contributor delete")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def delete(self, study_id: int, user_id: int):
        study = Study.query.get(study_id)
        contributors = study.study_contributor
        db.session.delete(contributors)
        db.session.commit()
        return 204
