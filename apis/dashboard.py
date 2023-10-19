import json
from flask_restx import Namespace, Resource, fields
from core import utils
from apis.models.fairhub import FairhubDashboardModel
from apis.models.fairhub import FairhubRecruitmentDashboardDataModel
from __main__ import DASHBOARDS_CONFIG, MEMORY_CACHE

#
# Reference Globals
#

# Set API Namespace
api = Namespace("dashboard", description="Dashboard related operations")

#
# Register API Models
#

fairhubDashboardModel = api.model("FairhubDashboard", FairhubDashboardModel)

fairhubRecruitmentDashboardDataModel = api.inherit(
    "FairhubRecruitmentDashboardData",
    FairhubRecruitmentDashboardDataModel,
    {"data": fields.List(fields.Nested(FairhubRecruitmentDashboardDataModel))},
)

#
# Dashboard Endpoints
#


@api.route("/")
class DashboardsList(Resource):
    @api.doc("get_dashboards")
    @api.marshal_list_with(fairhubDashboardModel)
    def get(self):
        """
        Get list of all available dashboards
        """
        return DASHBOARDS_CONFIG["dashboards"]


#
# Study Dashboard Endpoints
#


@api.route("/study/<study_id>")
class RecruitmentDashboard(Resource):
    @api.doc("get_recruitment_dashboard")
    @api.marshal_with(fairhubRecruitmentDashboardDataModel)
    def get(self, study_id):
        """
        Get study dashboard
        """
        dashboard_data = MEMORY_CACHE.get(f"transform_study-dashboard_{study_id}")
        print(dashboard_data)
        return dashboard_data


@api.route("/study/<study_id>/visualization-module/<module_name>")
@api.param("module_name", "The name of the visualization module")
@api.response(404, "No visualization module with that name found.")
class RecruitmentDashboardModuleByName(Resource):
    @api.doc("get_recruitment_dashboard_module_by_name")
    @api.marshal_with(fairhubRecruitmentDashboardDataModel)
    def get(self, module_name):
        """
        Get study dashboard visualization module data by name
        """
        for module in STUDY_DASHBOARD["data"]:
            if module["module_name"] == module_name:
                return module
        api.abort(404)
