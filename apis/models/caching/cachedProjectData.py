from flask_restx import fields

CachedProjectDataModel = {
    "name": fields.String(required=True, description="Dashboard name"),
    "varname": fields.String(required=True, description="Dasboard varname"),
    "namespace": fields.String(required=True, description="Dashboard namespace"),
    "endpoint": fields.String(required=True, description="Dashboard endpoint"),
}
