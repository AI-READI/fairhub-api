from flask_restx import fields

StudyDashboardDataModel = {
    "module_name": fields.String(required=True, description="Visualization module name"),
    "gender": fields.String(required=True, description="Gender"),
    "sex": fields.String(required=True, description="Sex"),
    "race": fields.String(required=True, description="Race"),
    "ethnicity": fields.String(required=True, description="Ethnicity"),
    "ancestry": fields.String(required=True, description="Ancestry"),
    "phenotype": fields.String(required=True, description="Phenotype"),
    "a1c": fields.String(required=True, description="A1C"),
    "recruitment_status": fields.String(required=True, description="Recruitment status"),
    "consent_status": fields.String(required=True, description="Consent status"),
    "communication_status": fields.String(required=True, description="Communication status"),
    "device_status_es": fields.String(required=True, description="Device status - environmental sensor"),
    "device_status_cgm": fields.String(required=True, description="Device status - continuous glucose monitor"),
    "device_status_amw": fields.String(required=True, description="Device status - activity monitor watch"),
    "device_status_all": fields.String(required=True, description="Device status - all devices"),
    "intervention_status": fields.String(required=True, description="Intervention status")
}
