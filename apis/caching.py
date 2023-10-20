import os
import requests
import json
from flask import jsonify
from flask_restx import Namespace, Resource, fields

# Caching API Models
from apis.models.caching import CachedProjectDataModel
from apis.models.caching import CachedParticipantsDataModel
from apis.models.caching import CachedRecruitmentDashboardDataModel

# In-Memory Cache Data Models
from caching.cachemodel.dashboard import DashboardCacheModel
from caching.cachemodel.dashboard import RecruitmentDashboardCacheModel
from caching.cachemodel.participant import ParticipantCacheModel
from caching.cachemodel.redcap import REDCapProjectCacheModel

# CachingETL
from modules.etl.transforms import REDCapTransform
from modules.etl.transforms import ModuleTransform

# Import In-Memory Cache
from __main__ import MEMORY_CACHE

"""
TODO:

Pull from SQL database and get list of caching projects. We need:
  - Caching project/API Key
  - Modules that need to be loaded for that recruitment
"""

# Get Environment Variables
REDCAP_API_TOKEN = os.environ["REDCAP_API_TOKEN"]
REDCAP_API_URL = os.environ["REDCAP_API_URL"]
REDCAP_API_FORMAT = os.environ["REDCAP_API_FORMAT"]
REDCAP_PROJECT_NAME = os.environ["REDCAP_PROJECT_NAME"]
REDCAP_PROJECT_ID = os.environ["REDCAP_PROJECT_ID"]
REDCAP_DASHBOARD_REPORT_ID = os.environ["REDCAP_DASHBOARD_REPORT_ID"]

# Set API Namespace
api = Namespace("caching", description="Caching API methods")

#
# Register API Models
#

cachedProjectDataModel = api.model("CachedProjectData", CachedProjectDataModel)
cachedParticipantsDataModel = api.model(
    "CachedParticipantsData", CachedParticipantsDataModel
)
cachedRecruitmentDashboardDataModel = api.model(
    "CachedRecruitmentDashboardData", CachedRecruitmentDashboardDataModel
)

#
# Caching Endpoints
#


@api.route("/project/<project_id>/caches`", methods=["GET", "POST"])
class CachingProjectData(Resource):
    @api.doc("get_caching_project")
    @api.marshal_with(cachedProjectDataModel)
    def get(self):
        """
        Get Caching project
        """
        PyCapProject = Project(REDCAP_API_URL, REDCAP_API_TOKEN)
        participantValues = PyCapProject.export_report(242544)
        return participantValues

        # dashboard_data = MEMORY_CACHE.get(f"transform_study-dashboard_{study_id}")
        # print(dashboard_data)
        # return dashboard_data


@api.route("/reports/participants", methods=["GET", "POST"])
class CachingReportParticipantsData(Resource):
    @api.doc("get_caching_report_participants")
    @api.marshal_with(cachedParticipantsDataModel)
    def get(self):
        """
        Get Caching project
        """
        return

    def post(self):
        """
        Get Caching project
        """
        return


@api.route("/reports/recruitment-dashboard", methods=["GET", "POST"])
class CachingReportRecruitmentDashboardData(Resource):
    @api.doc("get_caching_report_recruitment_dashboard")
    @api.marshal_with(cachedRecruitmentDashboardDataModel)
    def get(self):
        """
        Get REDCap data & cache
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


# @api.route("/reports/participant-values", methods=["GET"])
# class CachingReportParticipantValuesData(Resource):
#     @api.doc("get_caching_report_participant_values_data")
#     @api.marshal_with(cachedReportParticipantValuesDataModel)
#     def get(self):
#         """
#         Get Caching project
#         """
#         response = requests.post(
#             REDCAP_API_URL,
#             data={
#                 "token": REDCAP_API_TOKEN,
#                 "content": "project",
#                 "format": REDCAP_API_FORMAT,
#                 "returnFormat": REDCAP_API_FORMAT,
#             },
#         )
#         return response.json()

# @api.route("/reports/repeat-surveys", methods=["GET"])
# class CachingReportRepeatSurveysData(Resource):
#     @api.doc("get_caching_report_repeat_surveys")
#     @api.marshal_with(cachedReportRepeatSurveysDataModel)
#     def get(self):
#         """
#         Get Caching project
#         """
#         response = requests.post(
#             REDCAP_API_URL,
#             data={
#                 "token": REDCAP_API_TOKEN,
#                 "content": "project",
#                 "format": REDCAP_API_FORMAT,
#                 "returnFormat": REDCAP_API_FORMAT,
#             },
#         )
#         return response.json()


# # This endpoint pulls the configured Caching report and caches it
# @api.route("/reports/survey-completions", methods=["GET"])
# class CachingReportSurveyCompletionsData(Resource):
#     @api.doc("get_caching_report_survey_completions")
#     @api.marshal_list_with(cachedReportSurveyCompletionsDataModel)
#     def get(self):
#         """
#         Get Caching report for recruitment dashboard Fairhub.io
#         """
#         response = requests.post(
#             REDCAP_API_URL,
#             data={
#                 "token": REDCAP_API_TOKEN,
#                 "format": REDCAP_API_FORMAT,
#                 "returnFormat": REDCAP_API_FORMAT,
#                 "report_id": REDCAP_DASHBOARD_REPORT_ID,
#                 "content": "report",
#                 "rawOrLabel": "raw",
#                 "rawOrLabelHeaders": "raw",
#                 "exportCheckboxLabel": "true",
#             },
#         )
#         modules = [
#             "overview",
#             "progress",
#             "demographics",
#             "phenotype",
#             "device",
#             "contact",
#         ]
#         transformed_data = {}
#         print(response)
#         for module in modules:
#             transformed_data[module] = getattr(transforms, module)()

#         return transformed_data


# @api.route("/reports/recruitment/dm/<dm>", methods=["GET"])
# @api.param("dm", "The Caching dm field value")
# class CachingReportRecruitmentDataByDM(Resource):
#     @api.doc("get_caching_report_recruitment_by_dm")
#     @api.marshal_list_with(cachedReportRecruitmentDataModel)
#     def get(self, dm):
#         """
#         Get Caching report records by data manager sign-off status
#         """
#         response = requests.post(
#             REDCAP_API_URL,
#             data={
#                 "token": REDCAP_API_TOKEN,
#                 "format": REDCAP_API_FORMAT,
#                 "returnFormat": REDCAP_API_FORMAT,
#                 "report_id": REDCAP_DASHBOARD_REPORT_ID,
#                 "content": "report",
#                 "rawOrLabel": "raw",
#                 "rawOrLabelHeaders": "raw",
#                 "exportCheckboxLabel": "true",
#             },
#         )
#         return [row for row in response.json() if row["dm"] == dm]


# @api.route("/reports/recruitment/siteid/<siteid>", methods=["GET"])
# @api.param("siteid", "The Caching siteid field value")
# class CachingReportRecruitmentDataBySiteid(Resource):
#     @api.doc("get_caching_report_recruitment_by_siteid")
#     @api.marshal_list_with(cachedReportRecruitmentDataModel)
#     def get(self, siteid):
#         """
#         Get Caching report records by data generation site id
#         """
#         response = requests.post(
#             REDCAP_API_URL,
#             data={
#                 "token": REDCAP_API_TOKEN,
#                 "format": REDCAP_API_FORMAT,
#                 "returnFormat": REDCAP_API_FORMAT,
#                 "report_id": REDCAP_DASHBOARD_REPORT_ID,
#                 "content": "report",
#                 "rawOrLabel": "raw",
#                 "rawOrLabelHeaders": "raw",
#                 "exportCheckboxLabel": "true",
#             },
#         )
#         return [row for row in response.json() if row["siteid"] == siteid]
