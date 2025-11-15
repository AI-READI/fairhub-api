"""Initialize the api system for the backend"""

from flask_restx import Api, Resource

from apis.dataset_metadata_namespace import api as dataset_metadata_namespace
from apis.study_metadata_namespace import api as study_metadata_namespace

from .authentication import api as authentication
from .contributor import api as contributors_api
from .dashboard import api as dashboard
from .dataset import api as dataset_api
from .dataset_metadata.dataset_access_rights import api as access_rights
from .dataset_metadata.dataset_alternate_identifier import api as alternate_identifier
from .dataset_metadata.dataset_data_management import api as dataset_data_management
from .dataset_metadata.dataset_team import api as dataset_team
from .dataset_metadata.dataset_healthsheet import api as healthsheet
from .dataset_metadata.dataset_other import api as dataset_other
from .dataset_metadata.dataset_related_identifier import api as related_identifier
from .dataset_metadata.dataset_general_information import api as general_information
from .file import api as file_api
from .participant import api as participants_api
from .redcap import api as redcap
from .study import api as study_api
from .study_metadata.study_arm import api as arm
from .study_metadata.study_central_contact import api as central_contact
from .study_metadata.study_description import api as study_description
from .study_metadata.study_design import api as design
from .study_metadata.study_eligibility import api as eligibility
from .study_metadata.study_intervention import api as intervention
from .study_metadata.study_location import api as location
from .study_metadata.study_overall_official import api as overall_official
from .study_metadata.study_oversight import api as oversight
from .study_metadata.study_status import api as status
from .study_metadata.study_team import api as sponsors
from .user import api as user
from .utils import api as utils

api = Api(
    title="FAIRHUB",
    description="The backend api system for the fairhub vue app",
    doc="/docs",
)

__all__ = [
    "dataset_metadata_namespace",
    "study_metadata_namespace",
    "authentication",
    "contributors_api",
    "dataset_api",
    "access_rights",
    "alternate_identifier",
    "dataset_data_management",
    "healthsheet",
    "dataset_other",
    "related_identifier",
    "api",
    "general_information",
    "participants_api",
    "study_api",
    "arm",
    "central_contact",
    "design",
    "eligibility",
    "intervention",
    "location",
    "oversight",
    "overall_official",
    "sponsors",
    "status",
    "user",
    "study_description",
    "dataset_team",
    "redcap",
    "dashboard",
    "utils",
    # "invite_general_users",
]


api.add_namespace(dataset_metadata_namespace)
api.add_namespace(study_metadata_namespace)
api.add_namespace(authentication)


@api.route("/echo", endpoint="echo")
class HelloEverynyan(Resource):
    """Test if the server is active"""

    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def get(self):
        """Returns a simple 'Server Active' message"""
        return "Server active!"


api.add_namespace(study_api)
api.add_namespace(file_api)
api.add_namespace(dataset_api)
api.add_namespace(participants_api)
api.add_namespace(contributors_api)
api.add_namespace(user)
api.add_namespace(utils)
api.add_namespace(redcap)
api.add_namespace(dashboard)
