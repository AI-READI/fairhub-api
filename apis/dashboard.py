import json, os
from flask_restx import Namespace, Resource, fields
from core import utils

# API Models
from apis.models.fairhub import FairhubDashboardModel
from apis.models.fairhub import FairhubDashboardDatumModel

# REDCap Data Visualization ETL Configuration
from modules.etl.config import redcapTransformConfig
from modules.etl.config import sexGenderTransformConfig
from modules.etl.config import raceEthnicityTransformConfig
from modules.etl.config import phenotypeTransformConfig
from modules.etl.config import studyWaypointsTransformConfig

# ETL Modules
from modules.etl import transforms

# Import Globals from Main
from __main__ import MEMORY_CACHE

# Set API Namespace
api = Namespace("dashboards", description="Dashboard related operations")

#
# Register API Models
#

fairhubDashboardModel = api.model("FairhubDashboard", FairhubDashboardModel)
fairhubDashboardDatumModel = api.model("FairhubDashboardDatumModel", FairhubDashboardDatumModel)
# Transform API Data Models
fairhubRecruitmentDashboardDataModel = api.model(
    "FairhubRecruitmentDashboardDataModel", {
        "name": fields.String(required=True, description="Dashboard name"),
        "data": fields.List(fields.Nested(fairhubDashboardDatumModel), required=True, description="Dashboard data"),
    }
)
fairhubRecruitmentDashboardCompoundDataModel = api.model(
    "FairhubRecruitmentDashboardCompoundDataModel", {
        "name": fields.String(required=True, description="Dashboard name"),
        "data": fields.List(fields.Nested(fairhubDashboardDatumModel), required=True, description="Dashboard data"),
    }
)
fairhubRecruitmentDashboardMixedDataModel = api.model(
    "FairhubRecruitmentDashboardMixedDataModel", {
        "name": fields.String(required=True, description="Dashboard name"),
        "data": fields.List(fields.Nested(fairhubDashboardDatumModel), required=True, description="Dashboard data"),
    }
)

#
# Dashboard Endpoints
#

@api.route("/<project_id>", methods=["GET"])
class DashboardsList(Resource):
    @api.doc("get_dashboards")
    @api.marshal_list_with(fairhubDashboardModel)
    def get(self, project_id: int):
        """
        Get list of all available dashboards
        """
        REDCAP_PROJECT_ID = os.environ["REDCAP_PROJECT_ID"]
        return {
            "name": "recruitment_dashboard",
            "namespace": "dashboard",
            "endpoint": f"project/{project_id}/recruitment_dashboard"
        }

#
# Study Dashboard Endpoints
#

@api.route("/<project_id>/recruitment_dashboard", methods=["GET"])
class RecruitmentDashboard(Resource):
    @api.doc("get_recruitment_dashboard")
    @api.marshal_with(fairhubRecruitmentDashboardDataModel, as_list=True)
    @MEMORY_CACHE.cached(timeout=60*60*24, key_prefix="recruitment_dashboard")
    def get(self, project_id: int):
        """
        Get study dashboard

        TODO: Will need to use project_id to query SQL/KeyVault to
        get the correct REDCap API URL and token. For now,
        we'll just assume we have access through globals.

        Similarly, report_id needs to be retrieved. However, this
        may present an issue with flask_restx because we won't know
        the REDCap schema ahead of time unless we define an opinion-
        ated report schema that future studies will have to implement
        on their REDCap projects.
        """

        # Load environment variables. This should be replaced by an
        # SQL or KeyVauld call
        REDCAP_API_URL = os.environ["REDCAP_API_URL"]
        REDCAP_API_TOKEN = os.environ["REDCAP_API_TOKEN"]
        from modules.etl.config import redcapTransformConfig

        # Insert into dictionary
        redcapTransformConfig |= {
            "redcap_api_url": REDCAP_API_URL,
            "redcap_api_key": REDCAP_API_TOKEN,
        }

        extract = transforms.REDCapTransform(config = redcapTransformConfig).merged

        cacheTransforms = [
            sexGenderTransformConfig,
            raceEthnicityTransformConfig,
            phenotypeTransformConfig,
            studyWaypointsTransformConfig
        ]

        # Structure Response
        response = []
        for module_method, config in cacheTransforms:
            transformer = getattr(transforms.ModuleTransform(config), module_method)(extract)
            response.append({
                "name": config["key"],
                "data": transformer.transformed
            })
        return response
