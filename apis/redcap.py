"""API routes for study redcap"""

from typing import Any, Union

from flask import request
from flask_restx import Namespace, Resource, fields
from jsonschema import ValidationError, validate

import model

from .authentication import is_granted

api = Namespace("Redcap", description="REDCap operations", path="/")

redcap_project_view_model = api.model(
    "RedcapProjectAPI",
    {
        "study_id": fields.String(required=True, description="Study ID"),
        "id": fields.String(required=True, description="REDCap project ID"),
        "title": fields.String(required=True, description="REDCap project title"),
        "api_pid": fields.String(required=True, description="REDCap project PID"),
        "api_url": fields.String(required=True, description="REDCap project API url"),
        "api_active": fields.Boolean(
            required=True, description="REDCap project is active"
        ),
    },
)

redcap_api_model = api.model(
    "RedcapProjectAPI",
    {
        "study_id": fields.String(required=True, description="Study ID"),
        "id": fields.String(required=True, description="REDCap project ID"),
        "title": fields.String(required=True, description="REDCap project title"),
        "api_pid": fields.String(required=True, description="REDCap project PID"),
        "api_key": fields.String(required=True, description="REDCap project API key"),
        "api_url": fields.String(required=True, description="REDCap project API url"),
        "api_active": fields.Boolean(
            required=True, description="REDCap project is active"
        ),
    },
)

# project_parser = reqparse.RequestParser()
# project_parser.add_argument("api_pid", type=str, help="REDCap project ID (pid)")


@api.route("/study/<study_id>/redcap")
class RedcapProjectAPILink(Resource):
    @api.doc("Get all REDCap project API links")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_project_view_model, as_list=True)
    def get(self, study_id: str):
        """Get all REDCap project API links"""
        study = model.Study.query.get(study_id)
        if not is_granted("view", study):
            return (
                "Access denied, you can not view the redcap projects for this study",
                403,
            )
        redcap_project_views = model.StudyRedcap.query.filter_by(study=study)
        redcap_project_views = [
            redcap_project_view.to_dict()
            for redcap_project_view in redcap_project_views
        ]
        return redcap_project_views, 201

    @api.doc("Create a REDCap project API link")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_api_model)
    def post(self, study_id: str):
        """Create REDCap project API link"""
        study = model.Study.query.get(study_id)
        if not is_granted("add_redcap", study):
            return "Access denied, you can not create a redcap project", 403
        # Schema validation
        data: Union[Any, dict] = request.json
        schema = {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "title",
                "api_pid",
                "api_url",
                "api_key",
                "api_active",
            ],
            "properties": {
                "title": {"type": "string", "minLength": 1},
                "api_pid": {"type": "string", "minLength": 5},
                "api_url": {"type": "string", "minLength": 1},
                "api_key": {"type": "string", "minLength": 32},
                "api_active": {"type": "boolean"},
            },
        }

        try:
            validate(request.json, schema)
        except ValidationError as e:
            return e.message, 400

        if len(data["title"]) < 1:
            return (
                f"""redcap title is required for redcap access:
                {data['title']}""",
                400,
            )
        if len(data["api_pid"]) < 1:
            return (
                f"""redcap api_pid is required for redcap access:
                {data['api_pid']}""",
                400,
            )
        if len(data["api_url"]) < 1:
            return (
                f"""redcap api_url is required for redcap access:
                {data['api_url']}""",
                400,
            )
        if len(data["api_key"]) < 1:
            return (
                f"""redcap api_key is required for redcap access:
                {data['api_key']}""",
                400,
            )
        if not isinstance(data["api_active"], bool):
            return (
                f"""redcap api_active is required for redcap access:
                {data['api_active']}""",
                400,
            )

        add_redcap_api = model.StudyRedcap.from_data(study, data)
        model.db.session.add(add_redcap_api)
        model.db.session.commit()
        add_redcap_api = add_redcap_api.to_dict()
        return add_redcap_api, 201


# @api.route("/study/<study_id>/redcap/add")
# class AddRedcapProjectAPI(Resource):
#     @api.response(200, "Success")
#     @api.response(400, "Validation Error")
#     @api.marshal_with(redcap_project_view_model)
#     def post(self, study_id: int):
#         """Create REDCap project API link"""
#         study = model.Study.query.get(study_id)
#         if not is_granted("add_redcap", study):
#             return "Access denied, you can not create a redcap project", 403
#         # Schema validation
#         data: Union[Any, dict] = request.json
#         schema = {
#             "type": "object",
#             "additionalProperties": False,
#             "required": [
#                 "title",
#                 "api_pid",
#                 "api_url",
#                 "api_key",
#                 "api_active",
#             ],
#             "properties": {
#                 "title": {"type": "string", "minLength": 1},
#                 "api_pid": {"type": "string", "minLength": 5},
#                 "api_url": {"type": "string", "minLength": 1},
#                 "api_key": {"type": "string", "minLength": 32},
#                 "api_active": {"type": "boolean"},
#             },
#         }

#         try:
#             validate(request.json, schema)
#         except ValidationError as e:
#             return e.message, 400

#         if len(data["title"]) < 1:
#             return (
#                 f"""redcap title is required for redcap access:
#                 {data['title']}""",
#                 400,
#             )
#         if len(data["api_pid"]) < 1:
#             return (
#                 f"""redcap api_pid is required for redcap access:
#                 {data['api_pid']}""",
#                 400,
#             )
#         if len(data["api_url"]) < 1:
#             return (
#                 f"""redcap api_url is required for redcap access:
#                 {data['api_url']}""",
#                 400,
#             )
#         if len(data["api_key"]) < 1:
#             return (
#                 f"""redcap api_key is required for redcap access:
#                 {data['api_key']}""",
#                 400,
#             )
#         if not isinstance(data["api_active"], bool):
#             return (
#                 f"""redcap api_active is required for redcap access:
#                 {data['api_active']}""",
#                 400,
#             )

#         add_redcap_api = model.StudyRedcap.from_data(study, data)
#         model.db.session.add(add_redcap_api)
#         model.db.session.commit()
#         add_redcap_api = add_redcap_api.to_dict()
#         return add_redcap_api, 201


@api.route("/study/<study_id>/redcap/<redcap_id>")
class RedcapProjectAPI(Resource):
    # Get a REDCap API Link
    @api.doc("Get a REDCap project API link")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_project_view_model)
    def get(self, study_id: str, redcap_id: str):
        """Get REDCap project API link"""
        study = model.db.session.query(model.Study).get(study_id)
        if not is_granted("view", study):
            return "Access denied, you can not get this redcap project", 403
        redcap_project_view: Any = model.db.session.query(model.StudyRedcap).get(
            redcap_id
        )
        redcap_project_view = redcap_project_view.to_dict()
        return redcap_project_view, 201

    # Update REDCap API Link
    @api.doc("Update a REDCap project API link")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_project_view_model)
    def put(self, study_id: str, redcap_id: str):
        """Update REDCap project API link"""
        study = model.Study.query.get(study_id)
        if not is_granted("update_redcap", study):
            return "Access denied, you can not modify this redcap project", 403
        # Schema validation
        data: Union[Any, dict] = request.json
        schema = {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "title",
                "api_pid",
                "api_url",
                "api_active",
            ],
            "properties": {
                "title": {"type": "string", "minLength": 1},
                "api_pid": {"type": "string", "minLength": 5},
                "api_url": {"type": "string", "minLength": 1},
                "api_active": {"type": "boolean"},
            },
        }
        try:
            validate(request.json, schema)
        except ValidationError as e:
            return e.message, 400

        if len(data["title"]) < 1:
            return (
                f"""redcap title is required for redcap access:
                {data['title']}""",
                400,
            )
        if len(data["api_pid"]) < 1:
            return (
                f"""redcap api_pid is required for redcap access and must be concordant:
                {data['api_pid']}""",
                400,
            )
        if len(data["api_url"]) < 1:
            return (
                f"""redcap api_url is required for redcap access:
                {data['api_url']}""",
                400,
            )
        if not isinstance(data["api_active"], bool):
            return (
                f"""redcap api_active is required for redcap access:
                {data['api_active']}""",
                400,
            )

        update_redcap_project_view = model.StudyRedcap.query.get(redcap_id)
        update_redcap_project_view.update(data)
        model.db.session.commit()
        update_redcap_project_view = update_redcap_project_view.to_dict()
        return update_redcap_project_view, 201

    # Delete REDCap API Link
    @api.doc("Delete a REDCap project API link")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_project_view_model)
    def delete(self, study_id: str, redcap_id: str):
        """Delete REDCap project API link"""
        study = model.Study.query.get(study_id)
        if not is_granted("delete_redcap", study):
            return "Access denied, you can not delete this redcap project", 403
        model.StudyRedcap.query.filter_by(id=redcap_id).delete()
        model.db.session.commit()
        return 204


# @api.route("/study/<study_id>/redcap")
# class EditRedcapProjectAPI(Resource):
#     @api.doc(parser=project_parser)
#     @api.response(200, "Success")
#     @api.response(400, "Validation Error")
#     @api.marshal_with(redcap_project_view_model)
#     def put(self, study_id: int):
#         """Update REDCap project API link"""
#         study = model.Study.query.get(study_id)
#         if not is_granted("update_redcap", study):
#             return "Access denied, you can not modify this redcap project", 403
#         # Schema validation
#         data: Union[Any, dict] = request.json
#         schema = {
#             "type": "object",
#             "additionalProperties": False,
#             "required": [
#                 "api_pid",
#                 "title",
#                 "api_url",
#                 "api_active",
#             ],
#             "properties": {
#                 "api_pid": {"type": "string", "minLength": 1, "maxLength": 12},
#                 "title": {"type": "string", "minLength": 1},
#                 "api_url": {"type": "string", "minLength": 1},
#                 "api_active": {"type": "boolean"},
#             },
#         }
#         try:
#             validate(request.json, schema)
#         except ValidationError as e:
#             return e.message, 400

#         if len(data["api_pid"]) < 1:
#             return (
#                 f"""redcap api_pid is required for redcap access:
#                 {data['api_pid']}""",
#                 400,
#             )
#         if len(data["title"]) < 1:
#             return (
#                 f"""redcap title is required for redcap access:
#                 {data['title']}""",
#                 400,
#             )
#         if len(data["api_url"]) < 1:
#             return (
#                 f"""redcap api_url is required for redcap access:
#                 {data['api_url']}""",
#                 400,
#             )
#         if not isinstance(data["api_active"], bool):
#             return (
#                 f"""redcap api_active is required for redcap access:
#                 {data['api_active']}""",
#                 400,
#             )
#         update_redcap_project_view = model.StudyRedcap.query.get(
#             data["api_pid"]
#         )
#         update_redcap_project_view.update(data)
#         model.db.session.commit()
#         update_redcap_project_view = update_redcap_project_view.to_dict()
#         return update_redcap_project_view, 201


# @api.route("/study/<study_id>/redcap")
# class DeleteRedcapProjectAPI(Resource):
#     @api.doc(parser=project_parser)
#     @api.response(200, "Success")
#     @api.response(400, "Validation Error")
#     @api.marshal_with(redcap_project_view_model)
#     def delete(self, study_id: int):
#         """Delete REDCap project API link"""
#         study = model.Study.query.get(study_id)
#         if not is_granted("delete_redcap", study):
#             return "Access denied, you can not delete this redcap project", 403
#         api_pid = project_parser.parse_args()["api_pid"]
#         model.StudyRedcap.query.filter_by(api_pid=api_pid).delete()
#         model.db.session.commit()
#         return 204
