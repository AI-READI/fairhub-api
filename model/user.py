from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY
import uuid
from .db import db


class User(db.Model):
    def __init__(self):
        self.id = str(uuid.uuid4())

    __tablename__ = "user"
    id = db.Column(db.CHAR(36), primary_key=True)
    affiliations = db.Column(ARRAY(String), nullable=False)
    email = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    orcid = db.Column(db.String, nullable=False)
    roles = db.Column(ARRAY(String), nullable=False)
    permission = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "affiliations": self.affiliations,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "orcid": self.orcid,
            "roles": self.roles,
            "permission": self.permission,
            "status": self.status,
        }

    @staticmethod
    def from_data(data):
        user = User()
        # for i in data.values():
        #     print(i)
        # study_contributor.id = data["id"]
        user.affiliations = data["affiliations"]
        user.email = data["email"]
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.orcid = data["orcid"]
        user.roles = data["roles"]
        user.permission = data["permission"]
        user.status = data["status"]
        return user
