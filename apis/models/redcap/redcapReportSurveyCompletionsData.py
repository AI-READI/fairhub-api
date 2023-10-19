from flask_restx import fields

REDCapReportSurveyCompletionsDataModel = {
    "studyid": fields.String(
        required=True, readonly=True, description="Study participant ID"
    ),
    "dm_i": fields.String(
        required=True,
        readonly=True,
        description="All data collected and validated through in-person visit",
    ),
    "dm_d": fields.String(
        required=True,
        readonly=True,
        description="All device data entered and validated",
    ),
}
