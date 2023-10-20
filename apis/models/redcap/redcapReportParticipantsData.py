from flask_restx import fields

REDCapReportParticipantsDataModel = {
    "studyid": fields.String(required=True, readonly=True, description="Study participant ID"),
    "dm_inperson_data_validated": fields.Integer(
        required=True,
        readonly=True,
        attribute='dm___i',
        description="All data collected and validated through in-person visit"
    ),
    "dm_device_data_validated": fields.Integer(
        required=True,
        readonly=True,
        attribute='dm___d',
        description="All device data entered and validated"
    ),
}
