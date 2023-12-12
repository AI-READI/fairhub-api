import datetime
import uuid
import random

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
        self.email_verified = False
        self.generate_token()

    db.Column(db.BigInteger, nullable=False)
    __tablename__ = "user"
    id = db.Column(db.CHAR(36), primary_key=True)
    email_address = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String, nullable=False, unique=True)
    hash = db.Column(db.String, nullable=False)
    created_at = db.Column(db.BigInteger, nullable=False)
    email_verified = db.Column(db.BOOLEAN, nullable=True)
    token = db.Column(db.String, nullable=False)
    token_generated = db.Column(db.BigInteger, nullable=False)

    study_contributors = db.relationship(
        "StudyContributor",
        back_populates="user",
        cascade="all, delete",
    )
    email_verification = db.relationship(
        "EmailVerification",
        back_populates="user",
        cascade="all, delete",)
    user_details = db.relationship(
        "UserDetails",
        uselist=False,
        back_populates="user",
        cascade="all, delete",)
    token_blacklist = db.relationship(
        "TokenBlacklist",
        back_populates="user",
        cascade="all, delete",)
    notification = db.relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete",)
    invited_contributors = db.relationship(
        "Invite",
        back_populates="user",
        lazy="dynamic",
        cascade="all, delete",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "email_address": self.email_address,
            "username": self.username,
            "first_name": self.user_details.first_name if self.user_details else None,
            "last_name": self.user_details.last_name if self.user_details else None,
            "email_verified": self.email_verified,
            "token": self.token
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

    def verify_token(self, token: str) -> bool:
        if token != self.token:
            return False
        current_time = datetime.datetime.now()
        datetime_obj = datetime.datetime.utcfromtimestamp(self.created_at)
        formatted_time = datetime_obj.strftime('%Y-%m-%d %H:%M:%S.%f')
        created_time = datetime.datetime.strptime(formatted_time, '%Y-%m-%d %H:%M:%S.%f')
        return created_time - current_time > datetime.timedelta(minutes=15)

    def generate_token(self) -> str:
        self.token = str(random.randint(10 ** (7 - 1), (10 ** 7) - 1))
        self.token_generated = datetime.datetime.now(datetime.timezone.utc).timestamp()

        return self.token

    def change_email(self, email: str):
        if email == self.email_address:
            return

        self.email_verified = False
        self.email_address = email
        self.generate_token()
