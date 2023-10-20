from flask_restx import fields

FairhubDashboardModel = {
    "name": fields.String(required=True, description="Name of dashboard"),
    "namespace": fields.String(required=True, description="Dashboard API namespace"),
    "endpoint": fields.String(required=True, description="Dashboard API endpoint"),
}

FairhubDashboardDatumModel = {
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
