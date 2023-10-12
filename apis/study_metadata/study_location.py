"""API routes for study location metadata"""
from flask import request
from flask_restx import Resource, fields

import model
from apis.study_metadata_namespace import api

from ..authentication import is_granted

study_location = api.model(
    "StudyLocation",
    {
        "id": fields.String(required=True),
        "facility": fields.String(required=True),
        "status": fields.String(required=True),
        "city": fields.String(required=True),
        "state": fields.String(required=True),
        "zip": fields.String(required=True),
        "country": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/metadata/location")
class StudyLocationResource(Resource):
    """Study Location Metadata"""

    @api.doc("location")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The study identifier")
    @api.marshal_with(study_location)
    def get(self, study_id: int):
        """Get study location metadata"""
        study_ = model.Study.query.get(study_id)

        study_location_ = study_.study_location

        sorted_study_location = sorted(study_location_, key=lambda x: x.created_at)

        return [s.to_dict() for s in sorted_study_location]

    def post(self, study_id: int):
        """Create study location metadata"""
        study_obj = model.Study.query.get(study_id)
        if not is_granted("study_metadata", study_obj):
            return "Access denied, you can not delete study", 403
        data = request.json
        list_of_elements = []
        for i in data:
            if "id" in i and i["id"]:
                study_location_ = model.StudyLocation.query.get(i["id"])
                study_location_.update(i)
                list_of_elements.append(study_location_.to_dict())
            elif "id" not in i or not i["id"]:
                study_location_ = model.StudyLocation.from_data(study_obj, i)
                model.db.session.add(study_location_)
                list_of_elements.append(study_location_.to_dict())

        model.db.session.commit()

        return list_of_elements


@api.route("/study/<study_id>/metadata/location/<location_id>")
class StudyLocationUpdate(Resource):
    """Study Location Metadata"""

    def delete(self, study_id: int, location_id: int):
        """Delete study location metadata"""
        study_obj = model.Study.query.get(study_id)
        if not is_granted("study_metadata", study_obj):
            return "Access denied, you can not delete study", 403
        study_location_ = model.StudyLocation.query.get(location_id)

        model.db.session.delete(study_location_)

        model.db.session.commit()

        return 204
