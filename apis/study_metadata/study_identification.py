"""API routes for study identification metadata"""
from flask_restx import Resource, fields
from flask import request
from model import Study, db, StudyIdentification, Identifiers


from apis.study_metadata_namespace import api


study_identification = api.model(
    "StudyIdentification",
    {
        "id": fields.String(required=True),
        "identifier": fields.String(required=True),
        "identifier_type": fields.String(required=True),
        "identifier_domain": fields.String(required=True),
        "identifier_link": fields.String(required=True),
        "secondary": fields.Boolean(required=True),
    },
)


@api.route("/study/<study_id>/metadata/identification")
class StudyIdentificationResource(Resource):
    """Study Identification Metadata"""

    @api.doc("identification")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The study identifier")
    # @api.marshal_with(study_identification)
    def get(self, study_id: int):
        """Get study identification metadata"""
        study_ = Study.query.get(study_id)

        identifiers = Identifiers(study_)

        return identifiers.to_dict()

    def post(self, study_id: int):
        """Create study identification metadata"""
        data = request.json

        study_obj = Study.query.get(study_id)

        primary = data["primary"]
        primary["secondary"] = False

        if "id" in primary and primary["id"]:
            study_identification_ = StudyIdentification.query.get(primary["id"])
            study_identification_.update(primary)
        elif "id" not in primary or not primary["id"]:
            study_identification_ = StudyIdentification.from_data(
                study_obj, primary, False
            )
            db.session.add(study_identification_)

        for i in data["secondary"]:
            i["secondary"] = True

            if "id" in i and i["id"]:
                study_identification_ = StudyIdentification.query.get(i["id"])
                study_identification_.update(i)
            elif "id" not in i or not i["id"]:
                study_identification_ = StudyIdentification.from_data(
                    study_obj, i, True
                )
                db.session.add(study_identification_)

        db.session.commit()

        identifiers = Identifiers(study_obj)

        return identifiers.to_dict()

    @api.route("/study/<study_id>/metadata/identification/<identification_id>")
    class StudyIdentificationdUpdate(Resource):
        """Study Identification Metadata"""

        def delete(self, study_id: int, identification_id: int):
            """Delete study identification metadata"""
            study_identification_ = StudyIdentification.query.get(identification_id)

            if not study_identification_.secondary:
                return 400, "primary identifier can not be deleted"

            db.session.delete(study_identification_)
            db.session.commit()

            return 204
