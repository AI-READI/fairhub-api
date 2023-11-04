"""API routes for redcap project"""
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

redcap_project_data = api.model(
    "RedcapProject",
    {
        "project_id": fields.String(required=True, readonly=True, description=""),
        "project_title": fields.String(required=True, readonly=True, description=""),
        "creation_time": fields.String(required=True, readonly=True, description=""),
        "production_time": fields.String(required=True, readonly=True, description=""),
        "in_production": fields.Boolean(r=True, description=""),
        "project_language": fields.String(required=True, readonly=True, description=""),
        "purpose": fields.Integer(required=True, readonly=True, description=""),
        "purpose_other": fields.Integer(required=True, readonly=True, description=""),
        "project_notes": fields.String(required=True, readonly=True, description=""),
        "custom_record_label": fields.String(
            required=True, readonly=True, description=""
        ),
        "secondary_unique_field": fields.String(
            required=True, readonly=True, description=""
        ),
        "is_longitudinal": fields.Boolean(required=True, readonly=True, description=""),
        "has_repeating_instruments_or_events": fields.Boolean(
            required=True, readonly=True, description=""
        ),
        "surveys_enabled": fields.Boolean(required=True, readonly=True, description=""),
        "scheduling_enabled": fields.Boolean(
            required=True, readonly=True, description=""
        ),
        "record_autonumbering_enabled": fields.Boolean(
            required=True, readonly=True, description=""
        ),
        "randomization_enabled": fields.Boolean(
            required=True, readonly=True, description=""
        ),
        "ddp_enabled": fields.Boolean(required=True, readonly=True, description=""),
        "project_irb_number": fields.String(
            required=True, readonly=True, description=""
        ),
        "project_grant_number": fields.String(
            required=True, readonly=True, description=""
        ),
        "project_pi_firstname": fields.String(
            required=True, readonly=True, description=""
        ),
        "project_pi_lastname": fields.String(
            required=True, readonly=True, description=""
        ),
        "display_today_now_button": fields.Boolean(
            required=True, readonly=True, description=""
        ),
        "missing_data_codes": fields.String(
            required=True, readonly=True, description=""
        ),
        "external_modules": fields.String(required=True, readonly=True, description=""),
        "bypass_branching_erase_field_prompt": fields.Boolean(
            required=True, readonly=True, description=""
        ),
    },
)


@api.route("/study/<study_id>/redcap/<redcap_project_id>/project")
class RedcapProjectDataResource(Resource):
    """RedcapProjectDataResource"""

    @api.doc("project")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_project_data)
    def get(
        self, study_id: int, redcap_project_id: str
    ):  # pylint: disable=unused-argument
        """
        Get REDCap project

        TODO: Will need to use project_id to query SQL/KeyVault to
        get the correct REDCap API URL and token. For now,
        we'll just assume we have access through globals.
        """
        study_ = model.Study.query.get(study_id)
        study_redcap_ = study_.study_redcap.to_dict()
        PyCapProject = Project(
            study_redcap_["redcap_api_url"], study_redcap_["redcap_api_token"]
        )
        return PyCapProject.export_project_info()
