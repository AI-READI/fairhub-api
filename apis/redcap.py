import os
import requests
import json
from flask import jsonify
from flask_restx import Namespace, Resource, fields
from core import transforms
from model.dashboards import ProjectCache, REDCapReportStudyDashboardCache, DashboardCache, StudyDashboardCache
from apis.models import REDCapProjectDataModel
from apis.models import REDCapReportStudyDashboardDataModel
from __main__ import MEMORY_CACHE

"""TODO
Pull from SQL database and get list of redcap projects. We need:
    - REDCap project/API Key
    - Modules that need to be loaded for that study
"""

# Get Environment Variables
REDCAP_API_TOKEN = os.environ["REDCAP_API_TOKEN"]
REDCAP_API_URL = os.environ["REDCAP_API_URL"]
REDCAP_API_FORMAT = os.environ["REDCAP_API_FORMAT"]
REDCAP_PROJECT_NAME = os.environ["REDCAP_PROJECT_NAME"]
REDCAP_PROJECT_ID = os.environ["REDCAP_PROJECT_ID"]
REDCAP_DASHBOARD_REPORT_ID = os.environ["REDCAP_DASHBOARD_REPORT_ID"]

# Set API Namespace
api = Namespace("redcap", description="REDCap API methods")

#
# Register API Models
#

redcapProjectDataModel = api.model("REDCapProjectData", REDCapProjectDataModel)
redcapReportStudyDashboardDataModel = api.model(
    "REDCapReportStudyDashboardData", REDCapReportStudyDashboardDataModel
)

#
# REDCap Endpoints
#


@api.route("/project", methods=["GET"])
class REDCapProjectData(Resource):
    @api.doc("get_redcap_project")
    @api.marshal_with(redcapProjectDataModel)
    def get(self):
        """
        Get REDCap project
        """
        response = requests.post(
            REDCAP_API_URL,
            data={
                "token": REDCAP_API_TOKEN,
                "content": "project",
                "format": REDCAP_API_FORMAT,
                "returnFormat": REDCAP_API_FORMAT,
            },
        )
        return response.json()

# This endpoint pulls the configured REDCap report and caches it
@api.route("/reports/study-dashboard", methods=["GET"])
class REDCapReportStudyDashboardData(Resource):
    @api.doc("get_redcap_report_study_dashboard")
    @api.marshal_list_with(redcapReportStudyDashboardDataModel)
    def get(self):
        """
        Get REDCap report for study dashboard Fairhub.io
        """
        # dashboard_data = {
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
        # dashboard_data = transforms.redcap_to_redis_study_dashboard(dashboard_data)
        # MEMORY_CACHE.set(
        #     "transform_study-dashboard",
        #     dashboard_data
        # )
        response = requests.post(
            REDCAP_API_URL,
            data = {
                "token": REDCAP_API_TOKEN,
                "format": REDCAP_API_FORMAT,
                "returnFormat": REDCAP_API_FORMAT,
                "report_id": REDCAP_DASHBOARD_REPORT_ID,
                "content": "report",
                "rawOrLabel": "raw",
                "rawOrLabelHeaders": "raw",
                "exportCheckboxLabel": "true",
            },
        )
        modules = [
            "overview",
            "progress",
            "demographics",
            "phenotype",
            "device",
            "contact"
        ]
        transformed_data = {}
        for module in modules:
            transformed_data[module] = getattr(transforms, module)

        return transformed_data


@api.route("/reports/study-dashboard/dm/<dm>", methods=["GET"])
@api.param("dm", "The REDCap dm field value")
class REDCapReportStudyDashboardDataByDM(Resource):
    @api.doc("get_redcap_report_study_dashboard_by_dm")
    @api.marshal_list_with(redcapReportStudyDashboardDataModel)
    def get(self, dm):
        """
        Get REDCap report records by data manager sign-off status
        """
        response = requests.post(
            REDCAP_API_URL,
            data={
                "token": REDCAP_API_TOKEN,
                "format": REDCAP_API_FORMAT,
                "returnFormat": REDCAP_API_FORMAT,
                "report_id": REDCAP_DASHBOARD_REPORT_ID,
                "content": "report",
                "rawOrLabel": "raw",
                "rawOrLabelHeaders": "raw",
                "exportCheckboxLabel": "true",
            },
        )
        return [row for row in response.json() if row["dm"] == dm]


@api.route("/reports/study-dashboard/siteid/<siteid>", methods=["GET"])
@api.param("siteid", "The REDCap siteid field value")
class REDCapReportStudyDashboardDataBySiteid(Resource):
    @api.doc("get_redcap_report_study_dashboard_by_siteid")
    @api.marshal_list_with(redcapReportStudyDashboardDataModel)
    def get(self, siteid):
        """
        Get REDCap report records by data generation site id
        """
        response = requests.post(
            REDCAP_API_URL,
            data={
                "token": REDCAP_API_TOKEN,
                "format": REDCAP_API_FORMAT,
                "returnFormat": REDCAP_API_FORMAT,
                "report_id": REDCAP_DASHBOARD_REPORT_ID,
                "content": "report",
                "rawOrLabel": "raw",
                "rawOrLabelHeaders": "raw",
                "exportCheckboxLabel": "true",
            },
        )
        return [row for row in response.json() if row["siteid"] == siteid]


@api.route("/reports/study-dashboard/recordid/<recordid>", methods=["GET"])
@api.param("recordid", "The REDCap record_id field value")
class REDCapReportStudyDashboardDataByRecordid(Resource):
    @api.doc("get_redcap_report_study_dashboard_by_recordid")
    @api.marshal_list_with(redcapReportStudyDashboardDataModel)
    def get(self, recordid):
        """
        Get REDCap report records by record id
        """
        response = requests.post(
            REDCAP_API_URL,
            data={
                "token": REDCAP_API_TOKEN,
                "format": REDCAP_API_FORMAT,
                "returnFormat": REDCAP_API_FORMAT,
                "report_id": REDCAP_DASHBOARD_REPORT_ID,
                "content": "report",
                "rawOrLabel": "raw",
                "rawOrLabelHeaders": "raw",
                "exportCheckboxLabel": "true",
            },
        )
        return [row for row in response.json() if row["record_id"] == recordid]
