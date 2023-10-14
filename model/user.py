import datetime
import uuid

import app
import model

from .db import db

# from datetime import datetime, timezone


class User(db.Model):  # type: ignore
    def __init__(self, password):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
        self.set_password(password)
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
        user = User(data["password"])
        user.update(data)
        return user

    def update(self, data):
        self.email_address = data["email_address"]
        self.username = (
            data["username"] if "username" in data else data["email_address"]
        )
        # self.email_verified = data["email_verified"]
        # self.username = data["username"]
        # self.hash = data["hash"]
        # self.created_at = data["created_at"]

    def set_password(self, password: str):
        """setting bcrypt passwords"""
        hashed_password = app.bcrypt.generate_password_hash(password).decode("utf-8")
        self.hash = hashed_password

    def check_password(self, password: str):
        """validates password and bcrypt hashed password"""
        # TODO check password length and make uppercase letter
        app.bcrypt.generate_password_hash(password).decode("utf-8")
        is_valid = app.bcrypt.check_password_hash(self.hash, password)
        return is_valid
