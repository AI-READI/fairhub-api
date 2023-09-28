import uuid
from ..db import db
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY


class StudyIpdsharing(db.Model):
    """A study is a collection of datasets and participants"""

    def __init__(self, study):
        self.id = str(uuid.uuid4())
        self.study = study
        self.ipd_sharing = ""
        self.ipd_sharing_description = ""
        self.ipd_sharing_info_type_list = []
        self.ipd_sharing_time_frame = ""
        self.ipd_sharing_access_criteria = ""
        self.ipd_sharing_url = ""

    __tablename__ = "study_ipdsharing"

    id = db.Column(db.CHAR(36), primary_key=True)
    ipd_sharing = db.Column(db.String, nullable=False)
    ipd_sharing_description = db.Column(db.String, nullable=False)
    ipd_sharing_info_type_list = db.Column(ARRAY(String), nullable=False)
    ipd_sharing_time_frame = db.Column(db.String, nullable=False)
    ipd_sharing_access_criteria = db.Column(db.String, nullable=False)
    ipd_sharing_url = db.Column(db.String, nullable=False)

    study_id = db.Column(db.CHAR(36), db.ForeignKey("study.id", ondelete="CASCADE"), nullable=False)
    study = db.relationship("Study", back_populates="study_ipdsharing")

    def to_dict(self):
        """Converts the study to a dictionary"""
        return {
            "id": self.id,
            "ipd_sharing": self.ipd_sharing,
            "ipd_sharing_description": self.ipd_sharing_description,
            "ipd_sharing_info_type_list": self.ipd_sharing_info_type_list,
            "ipd_sharing_time_frame": self.ipd_sharing_time_frame,
            "ipd_sharing_access_criteria": self.ipd_sharing_access_criteria,
            "ipd_sharing_url": self.ipd_sharing_url,
        }

    @staticmethod
    def from_data(study, data: dict):
        """Creates a new study from a dictionary"""
        study_ipdsharing = StudyIpdsharing(study)
        study_ipdsharing.update(data)

        return study_ipdsharing

    def update(self, data):
        """Updates the study from a dictionary"""
        self.ipd_sharing = data["ipd_sharing"]
        self.ipd_sharing_description = data["ipd_sharing_description"]
        self.ipd_sharing_info_type_list = data["ipd_sharing_info_type_list"]
        self.ipd_sharing_time_frame = data["ipd_sharing_time_frame"]
        self.ipd_sharing_access_criteria = data["ipd_sharing_access_criteria"]
        self.ipd_sharing_url = data["ipd_sharing_url"]
        self.study.touch()

    def validate(self):
        """Validates the lead_sponsor_last_name study"""
        violations = []
        return violations
