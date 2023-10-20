import os
import requests
import json
from flask import jsonify
from flask_restx import Namespace, Resource, fields
from redcap import Project

# REDCap API Models
from apis.models.redcap import REDCapProjectDataModel
from apis.models.redcap import REDCapReportParticipantsDataModel
from apis.models.redcap import REDCapReportParticipantValuesDataModel
from apis.models.redcap import REDCapReportRepeatSurveysDataModel
from apis.models.redcap import REDCapReportSurveyCompletionsDataModel

# In-Memory Cache Data Models
from caching.cachemodel.dashboard import DashboardCacheModel
from caching.cachemodel.dashboard import RecruitmentDashboardCacheModel
from caching.cachemodel.participant import ParticipantCacheModel
from caching.cachemodel.redcap import REDCapProjectCacheModel

# REDCapETL
from modules.etl.transforms import REDCapTransform
from modules.etl.transforms import ModuleTransform

# Import In-Memory Cache
from __main__ import MEMORY_CACHE

"""
TODO:

Pull from SQL database and get list of redcap projects. We need:
  - REDCap project/API Key
  - Modules that need to be loaded for that recruitment
"""

# Get Environment Variables
REDCAP_API_TOKEN = os.environ["REDCAP_API_TOKEN"]
REDCAP_API_URL = os.environ["REDCAP_API_URL"]
REDCAP_API_FORMAT = os.environ["REDCAP_API_FORMAT"]
REDCAP_PROJECT_NAME = os.environ["REDCAP_PROJECT_NAME"]
REDCAP_PROJECT_ID = os.environ["REDCAP_PROJECT_ID"]

# Set API Namespace
api = Namespace("redcap", description="REDCap API methods")

#
# Register API Models
#

redcapProjectDataModel = api.model(
    "REDCapProjectData", REDCapProjectDataModel
)
redcapReportParticipantsDataModel = api.model(
    "REDCapReportParticipantsDashboardData", REDCapReportParticipantsDataModel
)
redcapReportParticipantValuesDataModel = api.model(
    "REDCapReportParticipantValuesData", REDCapReportParticipantValuesDataModel
)
redcapReportRepeatSurveysDataModel = api.model(
    "REDCapReportRepeatSurveysData", REDCapReportRepeatSurveysDataModel
)
redcapReportSurveyCompletionsDataModel = api.model(
    "REDCapReportSurveyCompletionsData", REDCapReportSurveyCompletionsDataModel
)

#
# REDCap Endpoints
#


@api.route("/project/<project_id>", methods=["GET"])
class REDCapProjectData(Resource):
    @api.doc("get_redcap_project")
    @api.marshal_with(redcapProjectDataModel)
    def get(self, project_id):
        """
        Get REDCap project

        TODO: Will need to use project_id to query SQL/KeyVault to
        get the correct REDCap API URL and token. For now,
        we'll just assume we have access through globals.
        """
        PyCapProject = Project(REDCAP_API_URL, REDCAP_API_TOKEN)
        project = PyCapProject.export_project_info()
        return project

# @api.route("/project/<project_id>/reports/<report_id>", methods=["GET"])
# class REDCapProjectData(Resource):
#     @api.doc("get_redcap_project")
#     @api.marshal_with(redcapProjectDataModel)
#     def get(self, project_id: int = 86847, report_id: int = None):
#         """
#         Get REDCap report by IDs

#         TODO: Will need to use project_id to query SQL/KeyVault to
#         get the correct REDCap API URL and token. For now,
#         we'll just assume we have access through globals.

#         Similarly, report_id needs to be retrieved. However, this
#         may present an issue with flask_restx because we won't know
#         the REDCap schema ahead of time unless we define an opinion-
#         ated report schema that future studies will have to implement
#         on their REDCap projects.
#         """
#         PyCapProject = Project(REDCAP_API_URL, REDCAP_API_TOKEN)
#         project = PyCapProject.export_project_info()
#         return project

@api.route("/project/<project_id>/reports/participants", methods=["GET"])
class REDCapReportParticipantsData(Resource):
    @api.doc("get_redcap_report_participants")
    @api.marshal_with(redcapReportParticipantsDataModel)
    def get(self, project_id: int):
        """
        Get REDCap project

        TODO: Will need to use project_id to query SQL/KeyVault to
        get the correct REDCap API URL and token. For now,
        we'll just assume we have access through globals.
        """
        PyCapProject = Project(REDCAP_API_URL, REDCAP_API_TOKEN)
        participants = PyCapProject.export_report(247884)
        return participants

@api.route("/project/<project_id>/reports/participant-values", methods=["GET"])
class REDCapReportParticipantValuesData(Resource):
    @api.doc("get_redcap_report_participant_values_data")
    @api.marshal_with(redcapReportParticipantValuesDataModel)
    def get(self, project_id: int):
        """
        Get REDCap project
        """
        PyCapProject = Project(REDCAP_API_URL, REDCAP_API_TOKEN)
        participantValues = PyCapProject.export_report(242544)
        return participantValues

@api.route("/project/<project_id>/reports/repeat-surveys", methods=["GET"])
class REDCapReportRepeatSurveysData(Resource):
    @api.doc("get_redcap_report_repeat_surveys")
    @api.marshal_with(redcapReportRepeatSurveysDataModel)
    def get(self, project_id: int):
        """
        Get REDCap project
        """
        PyCapProject = Project(REDCAP_API_URL, REDCAP_API_TOKEN)
        repeatSurveys = PyCapProject.export_report(259920)
        return repeatSurveys

# This endpoint pulls the configured REDCap report and caches it
@api.route("/project/<project_id>/reports/survey-completions", methods=["GET"])
class REDCapReportSurveyCompletionsData(Resource):
    @api.doc("get_redcap_report_survey_completions")
    @api.marshal_list_with(redcapReportSurveyCompletionsDataModel)
    def get(self, project_id: int):
        """
        Get REDCap report for recruitment dashboard Fairhub.io
        """
        PyCapProject = Project(REDCAP_API_URL, REDCAP_API_TOKEN)
        surveyCompletions = PyCapProject.export_report(251954)
        return surveyCompletions
