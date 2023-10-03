"""API routes for study overall official metadata"""
from flask_restx import Resource, fields
from flask import request
from model import Study, db, StudyOverallOfficial


from apis.study_metadata_namespace import api


study_overall_official = api.model(
    "StudyOverallOfficial",
    {
        "id": fields.String(required=True),
        "name": fields.String(required=True),
        "affiliation": fields.String(required=True),
        "role": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/metadata/overall-official")
class StudyOverallOfficialResource(Resource):
    """Study Overall Official Metadata"""

    @api.doc("overall_official")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The study identifier")
    # @api.marshal_with(study_overall_official)
    def get(self, study_id: int):
        """Get study overall official metadata"""
        study_ = Study.query.get(study_id)

        study_overall_official_ = study_.study_overall_official

        # sorted_by_date = sorted([i.created_at for i in study_overall_official_])

        sorted_study_overall = sorted(
            study_overall_official_, key=lambda x: x.created_at
        )

        return [i.to_dict() for i in sorted_study_overall]

    def post(self, study_id: int):
        """Create study overall official metadata"""
        data = request.json

        study_obj = Study.query.get(study_id)

        list_of_elements = []

        for i in data:
            if "id" in i and i["id"]:
                study_overall_official_ = StudyOverallOfficial.query.get(i["id"])
                study_overall_official_.update(i)
                list_of_elements.append(study_overall_official_.to_dict())
            elif "id" not in i or not i["id"]:
                study_overall_official_ = StudyOverallOfficial.from_data(study_obj, i)
                db.session.add(study_overall_official_)
                list_of_elements.append(study_overall_official_.to_dict())

        db.session.commit()

        return list_of_elements

    @api.route("/study/<study_id>/metadata/overall-official/<overall_official_id>")
    class StudyOverallOfficialUpdate(Resource):
        """Study Overall Official Metadata"""

        def delete(self, study_id: int, overall_official_id: int):
            """Delete study overall official metadata"""
            study_overall_official_ = StudyOverallOfficial.query.get(
                overall_official_id
            )

            db.session.delete(study_overall_official_)

            db.session.commit()

            return 204
