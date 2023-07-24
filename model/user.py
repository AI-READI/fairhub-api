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
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    ORCID = db.Column(db.String, nullable=False)
    roles = db.Column(ARRAY(String), nullable=False)
    permission = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "affiliations": self.affiliations,
            "email": self.email,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "ORCID": self.ORCID,
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
        user.firstname = data["firstname"]
        user.lastname = data["lastname"]
        user.ORCID = data["ORCID"]
        user.roles = data["roles"]
        user.permission = data["permission"]
        user.status = data["status"]
        return user
