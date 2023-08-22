"""Initialize the api system for the backend"""
from flask_restx import Api, Resource

from .cats import api as cats_api
from .contributor import api as contributors_api
from .dataset import api as dataset_api
from .participant import api as participants_api
from .study import api as study_api

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


api = Api(
    title="FAIRHUB",
    description="The backend api system for the fairhub vue app",
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

api.add_namespace(arm)
api.add_namespace(available_ipd)
api.add_namespace(contact)
api.add_namespace(description)
api.add_namespace(design)
api.add_namespace(eligibility)
api.add_namespace(identification)
api.add_namespace(intervention)
api.add_namespace(ipdsharing)
api.add_namespace(link)
api.add_namespace(location)
# api.add_namespace(other)
# api.add_namespace(overall_official)
# api.add_namespace(reference)
# api.add_namespace(sponsors_collaborator)
# api.add_namespace(status)
