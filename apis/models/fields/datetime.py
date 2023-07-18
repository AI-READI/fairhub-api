from flask_restx import fields
from datetime import datetime

class FormattedDateTime(fields.Raw):
    def format(self, value):
        return datetime.fromisoformat(value).strftime("%Y-%m-%dZ%H:%M:%S")
