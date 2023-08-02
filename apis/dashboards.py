# Temporary Example Data
# STUDY_DASHBOARD = {
#     "name": "studyDashboard",
#     "namespace": "studyDashboard",
#     "endpoint": "/study-dashboard",
#     "data": [
#         {
#             "module_name": "overview",
#             "gender": "gender",
#             "sex": "male",
#             "race": "race",
#             "ethnicity": "ethnicity",
#             "ancestry": "ancestry",
#             "phenotype": "phenotype",
#             "a1c": "a1c",
#             "recruitment_status": "recruitment_status",
#             "consent_status": "consent_status",
#             "communication_status": "communication_status",
#             "device_status_es": "device_status_es",
#             "device_status_cgm": "device_status_cgm",
#             "device_status_amw": "device_status_amw",
#             "device_status_all": "device_status_all",
#             "intervention_status": "intervention_status",
#         },
#         {
#             "module_name": "participant",
#             "gender": "gender",
#             "sex": "female",
#             "race": "race",
#             "ethnicity": "ethnicity",
#             "ancestry": "ancestry",
#             "phenotype": "phenotype",
#             "a1c": "a1c",
#             "recruitment_status": "recruitment_status",
#             "consent_status": "consent_status",
#             "communication_status": "communication_status",
#             "device_status_es": "device_status_es",
#             "device_status_cgm": "device_status_cgm",
#             "device_status_amw": "device_status_amw",
#             "device_status_all": "device_status_all",
#             "intervention_status": "intervention_status",
#         },
#     ],
# }
#

import json
from flask_restx import Namespace, Resource, fields
from core import utils
from .models import DashboardModel
from .models import FairhubStudyDashboardDataModel
from __main__ import DASHBOARDS_CONFIG, MEMORY_CACHE

with open("config/simulation.json") as config:
    STUDY_DASHBOAD = json.load(config)

#
# Reference Globals
#

# Set API Namespace
api = Namespace("dashboards", description="Dashboard related operations")

#
# Register API Models
#

dashboardModel = api.model("Dashboard", DashboardModel)

fairhubStudyDashboardDataModel = api.model(
    "FairhubStudyDashboardData", FairhubStudyDashboardDataModel
)

fairhubStudyDashboardModel = api.inherit(
    "FairhubStudyDashboard",
    dashboardModel,
    {"data": fields.List(fields.Nested(fairhubStudyDashboardDataModel))},
)

#
# Dashboard Endpoints
#

@api.route("/")
class DashboardsList(Resource):
    @api.doc("get_dashboards")
    @api.marshal_list_with(dashboardModel)
    def get(self):
        """
        Get list of all available dashboards
        """
        return DASHBOARDS_CONFIG["dashboards"]

#
# Study Dashboard Endpoints
#

@api.route("/study/<study_id>")
class StudyDashboard(Resource):
    @api.doc("get_study_dashboard")
    @api.marshal_with(fairhubStudyDashboardModel)
    def get(self, study_id):
        """
        Get study dashboard
        """
        dashboard_data = MEMORY_CACHE.get(f"transform_study-overview_{study_id}")
        print(dashboard_data)
        return dashboard_data


@api.route("/study/<study_id>/visualization-module/<module_name>")
@api.param("module_name", "The name of the visualization module")
@api.response(404, "No visualization module with that name found.")
class StudyDashboardModuleByName(Resource):
    @api.doc("get_study_dashboard_module_by_name")
    @api.marshal_with(fairhubStudyDashboardDataModel)
    def get(self, module_name):
        """
        Get study dashboard visualization module data by name
        """
        for module in STUDY_DASHBOARD["data"]:
            if module["module_name"] == module_name:
                return module
        api.abort(404)
