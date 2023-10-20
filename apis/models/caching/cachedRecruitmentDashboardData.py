from flask_restx import fields

CachedDashboardDatumModel = {
	"name": fields.String(required=True, description="Visualization name"),
	"filterby": fields.String(required=False, description="Filter variable"),
	"group": fields.String(required=False, description="Group variable"),
	"subgroup": fields.String(required=False, description="Subgroup variable"),
	"color": fields.String(required=False, description="Color variable"),
	"value": fields.Integer(required=False, description="Value (categorical) variable"),
	"date": fields.String(required=False, description="Date (x-axis) variable"),
	"x": fields.Float(required=False, description="X-axis variable"),
	"y": fields.Float(required=False, description="Y-axis variable"),
}

CachedRecruitmentDashboardDataModel = {
    "name": fields.String(required=True, description="Dashboard name"),
    "varname": fields.String(required=True, description="Dasboard varname"),
    "namespace": fields.String(required=True, description="Dashboard namespace"),
    "endpoint": fields.String(required=True, description="Dashboard endpoint"),
    "data": fields.List(fields.Nested(CachedDashboardDatumModel), required=True, description="Dashboard data")
}
