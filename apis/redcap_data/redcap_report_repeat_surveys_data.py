"""API routes for redcap report repeat surveys data"""
# import typing

# from flask import request
from flask_restx import Resource, fields

# from jsonschema import ValidationError, validate

import model
from apis.redcap_data_namespace import api

# from ..authentication import is_granted

# # REDCap Data Visualization ETL Configuration
# from modules.etl.config import redcapTransformConfig
# from modules.etl.config import sexGenderTransformConfig
# from modules.etl.config import raceEthnicityTransformConfig
# from modules.etl.config import phenotypeTransformConfig
# from modules.etl.config import studyWaypointsTransformConfig

# # ETL Modules
# from modules.etl import transforms


# Import In-Memory Cache
# from __main__ import IN_MEMORY_CACHE

redcap_report_repeat_surveys_data = api.model(
    "RedcapReportRepeatSurveysData",
    {
        "record_id": fields.String(
            required=True, readonly=True, description="Study participant ID"
        ),
        "studyid": fields.String(
            required=True, readonly=True, description="Study participant ID"
        ),
        "current_medications_complete": fields.String(
            required=True,
            readonly=True,
            description="All data collected and validated through in-person visit",
        ),
        "redcap_repeat_instrument": fields.String(
            required=True,
            readonly=True,
            description="All device data entered and validated",
        ),
        "redcap_repeat_instance": fields.String(
            required=True,
            readonly=True,
            description="All device data entered and validated",
        ),
    },
)


@api.route("/study/<study_id>/redcap/<redcap_project_id>/repeat-surveys")
class RedcapReportRepeatSurveysDataResource(Resource):
    @api.doc("report_repeat_surveys_data")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_report_repeat_surveys_data)
    # @IN_MEMORY_CACHE.cached()
    def get(self, study_id: int, redcap_project_id: str):
        study_ = model.Study.query.get(study_id)
        study_redcap_ = study_.study_redcap.to_dict()
        PyCapProject = Project(
            study_redcap_["redcap_api_url"], study_redcap_["redcap_api_token"]
        )
        repeat_surveys = PyCapProject.export_report(
            study_redcap_["redcap_report_id_repeat_surveys"]
        )
        return repeat_surveys
