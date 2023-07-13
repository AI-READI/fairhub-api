from flask_restx import Namespace, Resource
from .models import FairhubAPIModel
import os

print(os.environ)

api = Namespace("/", description="Root level operations")

#
# Register API Models
#

fairhubAPIModel = api.model(
    "FairhubAPIModel", FairhubAPIModel
)

#
# Root Endpoints
#

@api.route("/")
class Index(Resource):
    def get(self):
        return

@api.route("/version")
class Version(Resource):
    @api.doc("get_api_version")
    @api.marshal_with(fairhubAPIModel)
    def get(self):
        """
        Get Fairhub API version
        """
        return {
            "name": os.environ["FLASK_APP_NAME"],
            "title": os.environ["FLASK_APP_TITLE"],
            "version": os.environ["FLASK_APP_VERSION"],
            "description": os.environ["FLASK_APP_DESCRIPTION"],
            "summary": os.environ["FLASK_APP_SUMMARY"],
            "license": os.environ["FLASK_APP_LICENSE"]
        }
