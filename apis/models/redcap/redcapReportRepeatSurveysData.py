from flask_restx import fields

REDCapReportRepeatSurveysDataModel = {
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
}
