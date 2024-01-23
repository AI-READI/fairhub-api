"""Utils Endpoints"""
from flask import request
from flask_restx import Namespace, Resource

from core.utils import request_json

api = Namespace("Utils", description="utils operations", path="/")


@api.route("/utils/requestjson")
class RequestJSON(Resource):
    """requestJSON Resource"""

    @api.doc("requestjson")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def get(self):
        """Get requestjson"""
        url = request.args.get("url")

        return request_json(url), 200
