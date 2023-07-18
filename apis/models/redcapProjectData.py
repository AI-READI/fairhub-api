from flask_restx import fields

REDCapProjectDataModel = {
    "project_id": fields.String(required=True, readonly=True, description=""),
    "project_title": fields.String(required=True, readonly=True, description=""),
    "creation_time": fields.String(required=True, readonly=True, description=""),
    "production_time": fields.String(required=True, readonly=True, description=""),
    "in_production": fields.Boolean(required=True, readonly=True, description=""),
    "project_language": fields.String(required=True, readonly=True, description=""),
    "purpose": fields.Integer(required=True, readonly=True, description=""),
    "purpose_other": fields.Integer(required=True, readonly=True, description=""),
    "project_notes": fields.String(required=True, readonly=True, description=""),
    "custom_record_label": fields.String(required=True, readonly=True, description=""),
    "secondary_unique_field": fields.String(
        required=True, readonly=True, description=""
    ),
    "is_longitudinal": fields.Boolean(required=True, readonly=True, description=""),
    "has_repeating_instruments_or_events": fields.Boolean(
        required=True, readonly=True, description=""
    ),
    "surveys_enabled": fields.Boolean(required=True, readonly=True, description=""),
    "scheduling_enabled": fields.Boolean(required=True, readonly=True, description=""),
    "record_autonumbering_enabled": fields.Boolean(
        required=True, readonly=True, description=""
    ),
    "randomization_enabled": fields.Boolean(
        required=True, readonly=True, description=""
    ),
    "ddp_enabled": fields.Boolean(required=True, readonly=True, description=""),
    "project_irb_number": fields.String(required=True, readonly=True, description=""),
    "project_grant_number": fields.String(required=True, readonly=True, description=""),
    "project_pi_firstname": fields.String(required=True, readonly=True, description=""),
    "project_pi_lastname": fields.String(required=True, readonly=True, description=""),
    "display_today_now_button": fields.Boolean(
        required=True, readonly=True, description=""
    ),
    "missing_data_codes": fields.String(required=True, readonly=True, description=""),
    "external_modules": fields.String(required=True, readonly=True, description=""),
    "bypass_branching_erase_field_prompt": fields.Boolean(
        required=True, readonly=True, description=""
    ),
}
