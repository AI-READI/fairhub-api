from flask_restx import fields

FairhubDashboardModel = {
    "name": fields.String(required=True, description="Name of dashboard"),
    "namespace": fields.String(required=True, description="Dashboard API namespace"),
    "endpoint": fields.String(required=True, description="Dashboard API endpoint"),
}
