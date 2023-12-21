"""Initialize the api system for the backend"""
from flask_restx import Api, Resource
from apis.dataset_metadata_namespace import api as dataset_metadata_namespace
from apis.study_metadata_namespace import api as study_metadata_namespace

from .authentication import api as authentication
from .contributor import api as contributors_api
from .dataset import api as dataset_api
from .dataset_metadata.dataset_access import api as access
from .dataset_metadata.dataset_alternate_identifier import api as alternate_identifier
from .dataset_metadata.dataset_consent import api as consent
from .dataset_metadata.dataset_contributor import api as dataset_contributor
from .dataset_metadata.dataset_date import api as date
from .dataset_metadata.dataset_de_ident_level import api as de_ident_level
from .dataset_metadata.dataset_description import api as description
from .dataset_metadata.dataset_funder import api as funder
from .dataset_metadata.dataset_other import api as dataset_other
from .dataset_metadata.dataset_record_keys import api as record_keys
from .dataset_metadata.dataset_related_item import api as related_item
from .dataset_metadata.dataset_rights import api as rights
from .dataset_metadata.dataset_subject import api as subject
from .dataset_metadata.dataset_title import api as title
from .file import api as file_api
from .invite_users import api as invite_general_users
from .participant import api as participants_api
from .study import api as study_api
from .study_metadata.study_arm import api as arm
from .study_metadata.study_available_ipd import api as available_ipd
from .study_metadata.study_contact import api as contact
from .study_metadata.study_description import api as study_description
from .study_metadata.study_design import api as design
from .study_metadata.study_eligibility import api as eligibility
from .study_metadata.study_identification import api as identification
from .study_metadata.study_intervention import api as intervention
from .study_metadata.study_ipdsharing import api as ipdsharing
from .study_metadata.study_link import api as link
from .study_metadata.study_location import api as location
from .study_metadata.study_other import api as other
from .study_metadata.study_overall_official import api as overall_official
from .study_metadata.study_reference import api as reference
from .study_metadata.study_sponsors_collaborators import api as sponsors_collaborator
from .study_metadata.study_status import api as status
from .user import api as user

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
    "access",
    "alternate_identifier",
    "consent",
    "date",
    "de_ident_level",
    "description",
    "funder",
    "dataset_other",
    "record_keys",
    "related_item",
    "api",
    "rights",
    "subject",
    "title",
    "participants_api",
    "study_api",
    "arm",
    "available_ipd",
    "contact",
    "design",
    "eligibility",
    "intervention",
    "ipdsharing",
    "link",
    "location",
    "other",
    "overall_official",
    "reference",
    "sponsors_collaborator",
    "status",
    "user",
    "identification",
    "study_description",
    "dataset_contributor",
    "invite_general_users",
]


api.add_namespace(dataset_metadata_namespace)
api.add_namespace(study_metadata_namespace)
api.add_namespace(authentication)
api.add_namespace(invite_general_users)


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
