from flask_restx import Namespace, Resource, fields
from model import Study, db, StudyLink
from flask import request


from apis.study_metadata_namespace import api


study_link = api.model(
    "StudyLink",
    {
        "id": fields.String(required=True),
        "url": fields.String(required=True),
        "title": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/metadata/link")
class StudyLinkResource(Resource):
    @api.doc("link")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The study identifier")
    @api.marshal_with(study_link)
    def get(self, study_id: int):
        study_ = Study.query.get(study_id)
        study_link_ = study_.study_link
        sorted_study_link_ = sorted(study_link_, key=lambda x: x.created_at)
        return [s.to_dict() for s in sorted_study_link_]

    def post(self, study_id: int):
        data = request.json
        study_obj = Study.query.get(study_id)
        list_of_elements = []
        for i in data:
            if "id" in i and i["id"]:
                study_link_ = StudyLink.query.get(i["id"])
                if study_link_ == None:
                    return f"Study link {i['id']} Id is not found", 404
                study_link_.update(i)
                list_of_elements.append(study_link_.to_dict())
            elif "id" not in i or not i["id"]:
                study_link_ = StudyLink.from_data(study_obj, i)
                db.session.add(study_link_)
                list_of_elements.append(study_link_.to_dict())

        db.session.commit()
        return list_of_elements

    @api.route("/study/<study_id>/metadata/link/<link_id>")
    class StudyLinkUpdate(Resource):
        def delete(self, study_id: int, link_id: int):
            study_link_ = StudyLink.query.get(link_id)
            db.session.delete(study_link_)
            db.session.commit()
            return 204
