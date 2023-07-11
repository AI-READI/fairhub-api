from flask_restx import fields

REDCapDataModel = {
    "meow": fields.String(required=True, description="The sound of a cat"),
    "moo": fields.String(required=True, description="The sound of a cow"),
    "oink": fields.String(required=True, description="The sound of a pig")
}
