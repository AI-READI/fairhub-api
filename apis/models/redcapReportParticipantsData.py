from flask_restx import fields

REDCapReportParticipantsDataModel = {
    "studyid": fields.String(required=True, readonly=True, description=""),
    "data_management_complete": fields.String(required=True, readonly=True, description=""),
}
