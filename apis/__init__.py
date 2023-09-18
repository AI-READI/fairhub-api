"""Initialize the api system for the backend"""
from flask_restx import Api, Resource

from apis.dataset_metadata_namespace import api as dataset_metadata_namespace
from apis.study_metadata_namespace import api as study_metadata_namespace

from .contributor import api as contributors_api

from .dataset import api as dataset_api
from .participant import api as participants_api
from .study import api as study_api
from .invited_contributor import api as invited_contributors

from .signup_user import api as signup
from .login import api as login

from .study_metadata.study_arm import api as arm
from .study_metadata.study_available_ipd import api as available_ipd
from .study_metadata.study_contact import api as contact
from .study_metadata.study_description import api as description
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


from .dataset_metadata.dataset_access import api as access
from .dataset_metadata.dataset_consent import api as consent
from .dataset_metadata.dataset_subject import api as subject
from .dataset_metadata.dataset_description import api as description
from .dataset_metadata.dataset_alternate_identifier import api as alternate_identifier
from .dataset_metadata.dataset_other import api as dataset_other
from .dataset_metadata.dataset_date import api as date
from .dataset_metadata.dataset_de_ident_level import api as de_ident_level
from .dataset_metadata.dataset_managing_organization import api as managing_organization
from .dataset_metadata.dataset_readme import api as readme
from .dataset_metadata.dataset_record_keys import api as record_keys
from .dataset_metadata.dataset_rights import api as rights
from .dataset_metadata.dataset_title import api as title
from .dataset_metadata.dataset_related_item import api as related_item
from .dataset_metadata.dataset_related_item_title import api as related_item_title
from .dataset_metadata.dataset_related_item_contributor import (
    api as related_item_contributor,
)
from .dataset_metadata.dataset_related_item_identifier import (
    api as related_item_identifier,
)
from .dataset_metadata.dataset_related_item_other import api as related_item_other
from .dataset_metadata.dataset_funder import api as funder


api = Api(
    title="FAIRHUB",
    description="The backend api system for the fairhub vue app",
    doc="/docs",
)


api.add_namespace(dataset_metadata_namespace)
api.add_namespace(study_metadata_namespace)
api.add_namespace(signup)
api.add_namespace(login)

@api.route("/echo", endpoint="echo")
class HelloWorld(Resource):
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def get(self):
        """Returns a simple 'Server Active' message"""

        return "Server active!"


api.add_namespace(study_api)
api.add_namespace(dataset_api)
api.add_namespace(participants_api)
api.add_namespace(contributors_api)
api.add_namespace(invited_contributors)

