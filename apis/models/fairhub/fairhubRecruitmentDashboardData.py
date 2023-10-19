from flask_restx import fields

FairhubRecruitmentDashboardModuleDataModel = {
    "name": fields.String(
        required=True, description="Module name"
    ),
    "filterby": fields.String(
        required=False, description="Filter name"
    ),
    "group": fields.String(
        required=False, description="Group name"
    ),
    "subgroup": fields.String(
        required=False, description="Subgroup name"
    ),
    "value": fields.String(
        required=False, description="Categorical value"
    ),
    "x": fields.String(
        required=False, description="X-axis value"
    ),
    "y": fields.String(
        required=False, description="Y-axis value"
    ),
}

FairhubRecruitmentDashboardDataModel = {
    "name": fields.String(
        required=True, description="Visualization module name"
    ),
    "modules": fields.List(
        fields.Nested(FairhubRecruitmentDashboardModuleDataModel))
}
