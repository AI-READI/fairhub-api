from flask_restx import fields

CachedParticipantsDataModel = {
    "studyid": fields.String(required=True, description="Participant studyid"),
    "dm__i": fields.String(
        required=True,
        description="All data collected and validated through In-Person Visit",
    ),
    "dm__d": fields.String(
        required=True, description="All device data entered and validated"
    ),
}
