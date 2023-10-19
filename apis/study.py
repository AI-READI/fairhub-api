from typing import Any, Union

from flask import g, request
from flask_restx import Namespace, Resource, fields, reqparse
from jsonschema import ValidationError, validate

import model

from .authentication import is_granted

api = Namespace("Study", description="Study operations", path="/")


study_model = api.model(
    "Study",
    {
        "title": fields.String(required=True, default=""),
        "image": fields.String(required=True, default=""),
    },
)


@api.route("/study")
class Studies(Resource):
    parser_study = reqparse.RequestParser(bundle_errors=True)
    parser_study.add_argument(
        "title", type=str, required=True, location="json", help="The title of the Study"
    )
    parser_study.add_argument(
        "image",
        type=list,
        required=True,
        location="json",
        help="The image for the Study",
    )

    @api.doc(description="Return a list of all studies")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(study_model)
    def get(self):
        """this code ensure each user access and see only allowed studies"""
        # studies = Study.query.filter(
        #     Study.study_contributors.any(User.id == g.user.id)
        # ).all()
        # studies = Study.query.filter(User.id == g.user.id).all()
        study_contributors = model.StudyContributor.query.filter(
            model.StudyContributor.user_id == g.user.id
        ).all()  # Filter contributors where user_id matches the user's id
        study_ids = [contributor.study_id for contributor in study_contributors]

        studies = model.Study.query.filter(model.Study.id.in_(study_ids)).all()
        return [s.to_dict() for s in studies]

    @api.expect(study_model)
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def post(self):
        """Create a new study"""
        # Schema validation
        schema = {
            "type": "object",
            "required": ["title", "image"],
            "additionalProperties": False,
            "properties": {
                "title": {"type": "string", "minLength": 1},
                "image": {"type": "string", "minLength": 1},
            },
        }

        try:
            validate(request.json, schema)
        except ValidationError as e:
            return e.message, 400

        data: Union[Any, dict] = request.json

        add_study = model.Study.from_data(data)
        model.db.session.add(add_study)
        study_id = add_study.id
        study_ = model.Study.query.get(study_id)
        study_contributor = model.StudyContributor.from_data(study_, g.user, "owner")
        model.db.session.add(study_contributor)
        model.db.session.commit()
        return study_.to_dict()


@api.route("/study/<study_id>")
class StudyResource(Resource):
    @api.doc(description="Get a study's details")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(study)
    def get(self, study_id: int):
        study1 = model.Study.query.get(study_id)
        return study1.to_dict()

    @api.expect(study_model)
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.doc(description="Update a study's details")
    def put(self, study_id: int):
        """Update a study"""
        # Schema validation
        schema = {
            "type": "object",
            "required": ["title", "image"],
            "additionalProperties": False,
            "properties": {
                "title": {"type": "string", "minLength": 1},
                "image": {"type": "string", "minLength": 1},
            },
        }

        try:
            validate(request.json, schema)
        except ValidationError as e:
            return e.message, 400

        update_study = model.Study.query.get(study_id)
        if not is_granted("update_study", update_study):
            return "Access denied, you can not modify", 403

        update_study.update(request.json)
        model.db.session.commit()
        return update_study.to_dict()

    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.doc(description="Delete a study")
    def delete(self, study_id: int):
        study = model.Study.query.get(study_id)
        if not is_granted("delete_study", study):
            return "Access denied, you can not delete study", 403
        for d in study.dataset:
            for version in d.dataset_versions:
                version.participants.clear()
        for d in study.dataset:
            for version in d.dataset_versions:
                model.db.session.delete(version)
            model.db.session.delete(d)
        for p in study.participants:
            model.db.session.delete(p)
        model.db.session.delete(study)
        model.db.session.commit()
        studies = model.Study.query.filter(
            model.Study.study_contributors.any(model.User.id == g.user.id)
        ).all()
        return [s.to_dict() for s in studies], 201
