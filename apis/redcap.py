from flask import request
from flask_restx import Namespace, Resource, fields
from core import utils
from .models import REDCapProjectDataModel
from .models import REDCapReportStudyDashboardDataModel
import os, requests, redis

# Get Environment Variables
REDCAP_CONFIG               = utils.load_json("config/redcap.json")
REDCAP_API_TOKEN            = os.environ["REDCAP_API_TOKEN"]
REDCAP_API_URL              = os.environ["REDCAP_API_URL"]
REDCAP_API_FORMAT           = os.environ["REDCAP_API_FORMAT"]
REDCAP_PROJECT_NAME         = os.environ["REDCAP_PROJECT_NAME"]
REDCAP_PROJECT_ID           = os.environ["REDCAP_PROJECT_ID"]
REDCAP_DASHBOARD_REPORT_ID  = os.environ["REDCAP_DASHBOARD_REPORT_ID"]

# Set API Namespace
api = Namespace("redcap", description="REDCap API methods")

#
# Register API Models
#

redcapProjectDataModel = api.model(
    "REDCapProjectData",
    REDCapProjectDataModel
)
redcapReportStudyDashboardDataModel = api.model(
    "REDCapReportStudyDashboardData",
    REDCapReportStudyDashboardDataModel
)

#
# REDCap Endpoints
#

@api.route("/project", methods=['GET'])
class REDCapProjectData(Resource):
    @api.doc("get_redcap_project")
    @api.marshal_with(redcapProjectDataModel)
    def get(self):
        """
        Get REDCap project
        """
        response = requests.post(
            REDCAP_API_URL, data = {
                'token': REDCAP_API_TOKEN,
                'content': 'project',
                'format': REDCAP_API_FORMAT,
                'returnFormat': REDCAP_API_FORMAT
            }
        )
        return response.json()

@api.route("/reports/study-dashboard", methods=["GET"])
class REDCapReportStudyDashboardData(Resource):
    @api.doc("get_redcap_report_study_dashboard")
    @api.marshal_list_with(redcapReportStudyDashboardDataModel)
    def get(self):
        """
        Get REDCap report for study dashboard Fairhub.io
        """
        response = requests.post(
            REDCAP_API_URL, data = {
                'token': REDCAP_API_TOKEN,
                'format': REDCAP_API_FORMAT,
                'returnFormat': REDCAP_API_FORMAT,
                'report_id': REDCAP_DASHBOARD_REPORT_ID,
                'content': 'report',
                'rawOrLabel': 'raw',
                'rawOrLabelHeaders': 'raw',
                'exportCheckboxLabel': 'true'
            }
        )
        return response.json()

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
            REDCAP_API_URL, data = {
                'token': REDCAP_API_TOKEN,
                'format': REDCAP_API_FORMAT,
                'returnFormat': REDCAP_API_FORMAT,
                'report_id': REDCAP_DASHBOARD_REPORT_ID,
                'content': 'report',
                'rawOrLabel': 'raw',
                'rawOrLabelHeaders': 'raw',
                'exportCheckboxLabel': 'true'
            }
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
            REDCAP_API_URL, data = {
                'token': REDCAP_API_TOKEN,
                'format': REDCAP_API_FORMAT,
                'returnFormat': REDCAP_API_FORMAT,
                'report_id': REDCAP_DASHBOARD_REPORT_ID,
                'content': 'report',
                'rawOrLabel': 'raw',
                'rawOrLabelHeaders': 'raw',
                'exportCheckboxLabel': 'true'
            }
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
            REDCAP_API_URL, data = {
                'token': REDCAP_API_TOKEN,
                'format': REDCAP_API_FORMAT,
                'returnFormat': REDCAP_API_FORMAT,
                'report_id': REDCAP_DASHBOARD_REPORT_ID,
                'content': 'report',
                'rawOrLabel': 'raw',
                'rawOrLabelHeaders': 'raw',
                'exportCheckboxLabel': 'true'
            }
        )
        return [row for row in response.json() if row["record_id"] == recordid]
