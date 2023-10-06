import uuid
from datetime import datetime
from .db import db
from datetime import timezone
import datetime
import app
import model


class User(db.Model):
    def __init__(self, password, data):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.datetime.now(timezone.utc).timestamp()
        self.set_password(password, data)
        self.user_details = model.UserDetails(self)

    __tablename__ = "user"
    id = db.Column(db.CHAR(36), primary_key=True)
    email_address = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String, nullable=False, unique=True)
    hash = db.Column(db.String, nullable=False)
    created_at = db.Column(db.BigInteger, nullable=False)
    email_verified = db.Column(db.String, nullable=True)

    study_contributors = db.relationship("StudyContributor", back_populates="user")
    email_verification = db.relationship("EmailVerification", back_populates="user")
    user_details = db.relationship("UserDetails", uselist=False, back_populates="user")

    def to_dict(self):
        return {
            "id": self.id,
            "email_address": self.email_address,
            "username": self.username,
            "first_name": self.user_details.first_name if self.user_details else None,
            "last_name": self.user_details.last_name if self.user_details else None,
        }

    @staticmethod
    def from_data(data: dict):
        user = User(data["password"], data)
        user.update(data)
        return user

    def update(self, data):
        self.email_address = data["email_address"]
        self.username = data["email_address"]
        # self.email_verified = data["email_verified"]
        # self.username = data["username"]
        # self.hash = data["hash"]
        # self.created_at = data["created_at"]

    def set_password(self, password, data):
        """setting bcrypt passwords"""
        hashed_password = app.bcrypt.generate_password_hash(password).decode("utf-8")
        self.hash = hashed_password

    def check_password(self, password):
        """validates password and bcrypt hashed password"""
        # TODO check password length and make uppercase letter
        hashed_password = app.bcrypt.generate_password_hash(password).decode("utf-8")
        is_valid = app.bcrypt.check_password_hash(hashed_password, password)
        return is_valid

    def add_study(self, user, permission):
        contributor = model.StudyContributor(self, permission)
