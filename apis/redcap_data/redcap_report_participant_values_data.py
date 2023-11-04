"""API routes for redcap report participant values data"""
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

redcap_report_participant_values_data = api.model(
    "RedcapReportParticipantValuesData",
    {
        "record_id": fields.String(
            required=True, readonly=True, description="Participant record ID"
        ),
        "studyid": fields.String(
            required=True, readonly=True, description="Study participant ID"
        ),
        "siteid": fields.String(required=True, readonly=True, description="Site ID"),
        "dm": fields.String(
            required=True, readonly=True, description="Data approved for Fairhub.io"
        ),
        "genderid": fields.String(
            required=True, readonly=True, description="Gender identity"
        ),
        "scrsex": fields.String(
            required=True, readonly=True, description="Sex at birth"
        ),
        "race": fields.String(required=True, readonly=True, description="Race"),
        "race2": fields.String(
            required=True, readonly=True, description="Race further defined"
        ),
        "ethnic": fields.String(required=True, readonly=True, description="Ethnicity"),
        "dvenvyn": fields.String(
            required=True, readonly=True, description="Environmental sensor distributed"
        ),
        "dvenvstdat": fields.String(
            required=True,
            readonly=True,
            description="Date of environmental sensor distribution",
        ),
        "dvenvcrcid": fields.String(
            required=True,
            readonly=True,
            description="Was environmental sensor demonstrated?",
        ),
        "dvcgmyn": fields.String(
            required=True,
            readonly=True,
            description="Continuous glucose monitor inserted",
        ),
        "dvcgmstdat": fields.String(
            required=True,
            readonly=True,
            description="Date of continuous glucose monitor was inserted",
        ),
        "dvcgmvrfy": fields.String(
            required=True,
            readonly=True,
            description="Continuous glucose monitor initialized and recording?",
        ),
        "dvamwyn": fields.String(
            required=True,
            readonly=True,
            description="Was the Apple watch sent home with the participant?",
        ),
        "dvamwstdat": fields.String(
            required=True,
            readonly=True,
            description="Date Apple watch was given to participant",
        ),
        "dvamwsn": fields.String(
            required=True, readonly=True, description="Apple watch serial number"
        ),
        "dvrtmthd": fields.String(
            required=True, readonly=True, description="Planned method of device return"
        ),
        "dvrtnyn": fields.String(
            required=True,
            readonly=True,
            description="Was the participant given device return instructions and shipping materials?",  # noqa: E501 # pylint: disable=line-too-long
        ),
        "dvrtnship": fields.String(
            required=True, readonly=True, description="Return shipping tracking number"
        ),
        "mhterm_dm1": fields.String(
            required=True, readonly=True, description="Type I diabetes"
        ),
        "mhterm_dm2": fields.String(
            required=True, readonly=True, description="Type II diabetes"
        ),
        "mhterm_predm": fields.String(
            required=True, readonly=True, description="Pre-diabetes"
        ),
        "mh_dm_age": fields.String(
            required=True,
            readonly=True,
            description="Age diagnosed with type II diabetes",
        ),
        "mh_a1c": fields.String(
            required=True, readonly=True, description="Elevated A1C levels"
        ),
        "cmtrt_a1c": fields.String(
            required=True,
            readonly=True,
            description="Taking pills to control A1C and blood glucose levels?",
        ),
        "cmtrt_insln": fields.String(
            required=True,
            readonly=True,
            description="Injecting insulin to control blood glucose levels",
        ),
        "cmtrt_glcs": fields.String(
            required=True,
            readonly=True,
            description="Using other injectables to control blood glucose levels",
        ),
        "cmtrt_lfst": fields.String(
            required=True,
            readonly=True,
            description="Using lifestyle changes to control blood glucose levels",
        ),
        "scrcmpdat": fields.String(
            required=True, readonly=True, description="Screening survey completion date"
        ),
    },
)


@api.route("/study/<study_id>/redcap/<redcap_project_id>/participant-values")
class RedcapReportParticipantValuesDataResource(Resource):
    @api.doc("report_participant_values_data")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_report_participant_values_data)
    # @IN_MEMORY_CACHE.cached()
    def get(
        self, study_id: int, redcap_project_id: str
    ):  # pylint: disable=unused-argument
        study_ = model.Study.query.get(study_id)
        study_redcap_ = study_.study_redcap.to_dict()
        PyCapProject = Project(
            study_redcap_["redcap_api_url"], study_redcap_["redcap_api_token"]
        )
        participant_values = PyCapProject.export_report(
            study_redcap_["redcap_report_id_participant_values"]
        )
        return participant_values
