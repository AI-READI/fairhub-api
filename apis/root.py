from flask_restx import Namespace, Resource
import os

from apis.models.fairhub import FairhubAPIModel

api = Namespace("/", description="Root level operations")

#
# Register API Models
#

fairhubApiModel = api.model("FairhubApiModel", FairhubAPIModel)

#
# Root Endpoints
#


@api.route("/")
class Index(Resource):
    @api.doc("get_api")
    @api.marshal_with(fairhubApiModel)
    def get(self):
        """
        Get Fairhub API
        """
        return {
            "name": os.environ["FLASK_APP_NAME"],
            "title": os.environ["FLASK_APP_TITLE"],
            "version": os.environ["FLASK_APP_VERSION"],
            "description": os.environ["FLASK_APP_DESCRIPTION"],
            "summary": os.environ["FLASK_APP_SUMMARY"],
            "license": os.environ["FLASK_APP_LICENSE"],
        }


@api.route("/version")
class Version(Resource):
    @api.doc("get_api_version")
    @api.marshal_with(fairhubApiModel)
    def get(self):
        """
        Get Fairhub API version - syntactic sugar for root method (get_api)
        """
        return {
            "name": os.environ["FLASK_APP_NAME"],
            "title": os.environ["FLASK_APP_TITLE"],
            "version": os.environ["FLASK_APP_VERSION"],
            "description": os.environ["FLASK_APP_DESCRIPTION"],
            "summary": os.environ["FLASK_APP_SUMMARY"],
            "license": os.environ["FLASK_APP_LICENSE"],
        }
