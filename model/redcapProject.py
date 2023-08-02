from __main__ import db


class REDCapProject(db.Model):
    __tablename__ = "redcapProject"
    id = db.Column(db.Integer, primary_key = True)
    study_id = db.Column(db.Integer)
    project_id = db.Column(db.String)
    project_name = db.Column(db.String)
    api_token = db.Column(db.String)
    api_url = db.Column(db.String)
    api_format = db.Column(db.String)
    dashboard_report_id = db.Column(db.String)
    dashbboard_report_modules =
    __table_args__ = (
        ForeignKeyConstraint(
            [study_id, project_id],
            [Study.id, project_id],
            {}
        )
    )
