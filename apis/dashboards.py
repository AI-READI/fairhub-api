# Temporary Example Data
STUDY_DASHBOARD = {
    "name": "studyDashboard",
    "namespace": "studyDashboard",
    "endpoint": "/study-dashboard",
    "data": [
        {
            "module_name": "overview",
            "gender": "gender",
            "sex": "male",
            "race": "race",
            "ethnicity": "ethnicity",
            "ancestry": "ancestry",
            "phenotype": "phenotype",
            "a1c": "a1c",
            "recruitment_status": "recruitment_status",
            "consent_status": "consent_status",
            "communication_status": "communication_status",
            "device_status_es": "device_status_es",
            "device_status_cgm": "device_status_cgm",
            "device_status_amw": "device_status_amw",
            "device_status_all": "device_status_all",
            "intervention_status": "intervention_status"
        }, {
            "module_name": "participant",
            "gender": "gender",
            "sex": "female",
            "race": "race",
            "ethnicity": "ethnicity",
            "ancestry": "ancestry",
            "phenotype": "phenotype",
            "a1c": "a1c",
            "recruitment_status": "recruitment_status",
            "consent_status": "consent_status",
            "communication_status": "communication_status",
            "device_status_es": "device_status_es",
            "device_status_cgm": "device_status_cgm",
            "device_status_amw": "device_status_amw",
            "device_status_all": "device_status_all",
            "intervention_status": "intervention_status"
        }
    ]
}
#


from flask_restx import Namespace, Resource, fields
from core import utils
from .models import DashboardModel
from .models import StudyDashboardDataModel

# Get Environment Variables
DASHBOARDS_CONFIG   = utils.load_json("config/dashboards.json")

# Set API Namespace
api = Namespace("dashboards", description="Dashboard related operations")

#
# Register API Models
#

dashboardModel = api.model(
    "Dashboard", DashboardModel
)

studyDashboardDataModel = api.model(
    "StudyDashboardData", StudyDashboardDataModel
)

studyDashboardModel = api.inherit(
    "StudyDashboard", dashboardModel, {
        "data": fields.List(fields.Nested(studyDashboardDataModel))
    }
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

@api.route("/study-dashboard")
class StudyDashboard(Resource):
    @api.doc("get_study_dashboard")
    @api.marshal_with(studyDashboardModel)
    def get(self):
        """
        Get study dashboard
        """
        return STUDY_DASHBOARD


@api.route("/study-dashboard/<module_name>")
@api.param("module_name", "The name of the visualization module")
@api.response(404, "No visualization module with that name found.")
class StudyDashboardModuleByName(Resource):
    @api.doc("get_study_dashboard_module_by_name")
    @api.marshal_with(studyDashboardDataModel)
    def get(self, module_name):
        """
        Get study dashboard visualization module data by name
        """
        for module in STUDY_DASHBOARD["data"]:
            if module["module_name"] == module_name:
                return module
        api.abort(404)
