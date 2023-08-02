"""Initialize the api system for the backend"""
from flask_restx import Api, Resource

from .cats import api as cats_api
from .contributor import api as contributors_api
from .dataset import api as dataset_api
from .participant import api as participants_api
from .study import api as study_api

api = Api(
    title="FAIRHUB",
    description="The backend api system for the Vue app",
    doc="/docs",
)


@api.route("/echo", endpoint="echo")
class HelloWorld(Resource):
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def get(self):
        """Returns a simple 'Server Active' message"""

        return "Server active!"


api.add_namespace(cats_api)
api.add_namespace(study_api)
api.add_namespace(dataset_api)
api.add_namespace(participants_api)
api.add_namespace(contributors_api)
