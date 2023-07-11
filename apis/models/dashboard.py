from flask_restx import fields

DashboardModel = {
    "name": fields.String(required=True, description="Name of dashboard"),
    "namespace": fields.String(required=True, description="Dashboard API namespace"),
    "endpoint": fields.String(required=True, description="Dashboard API endpoint")
}
