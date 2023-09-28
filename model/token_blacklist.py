
from .db import db


class TokenBlacklist(db.Model):
    __tablename__ = "token_blacklist"
    jti = db.Column(db.CHAR(36), primary_key=True)
    exp = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            "jti": self.jti,
            "exp": self.exp,
        }

    @staticmethod
    def from_data(data: dict):
        token_blacklist = TokenBlacklist()
        token_blacklist.update(data)
        return token_blacklist

    def update(self, data):
        self.jti = data["jti"]
        self.exp = data["exp"]
