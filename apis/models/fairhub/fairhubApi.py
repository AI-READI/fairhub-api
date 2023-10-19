from flask_restx import fields

FairhubAPIModel = {
    "name": fields.String(required=True, description="Fairhub.io API name"),
    "title": fields.String(required=True, description="Fairhub.io API title"),
    "version": fields.String(required=True, description="Fairhub.io API version"),
    "description": fields.String(
        required=True, description="Fairhub.io API description"
    ),
    "summary": fields.String(required=True, description="Fairhub.io API summary"),
    "license": fields.String(required=True, description="Fairhub.io API license"),
}
