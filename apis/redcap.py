# Temporary Example Data
REDCAP_DATA = [

]
#

from flask_restx import Namespace, Resource, fields
from core import utils
from .models import REDCapDataModel
import os

# Get Environment Variables
REDCAP_CONFIG       = utils.load_json("config/redcap.json")
REDCAP_API_TOKEN    = os.environ["REDCAP_API_TOKEN"]
REDCAP_API_URL      = os.environ["REDCAP_API_URL"]
REDCAP_PROJECT_NAME = os.environ["REDCAP_PROJECT_NAME"]
REDCAP_PROJECT_ID   = os.environ["REDCAP_PROJECT_ID"]

# Set API Namespace
api = Namespace("redcap", description="REDCap API methods")

#
# Register API Models
#

redcapDataModel = api.model(
    "REDCapData",
    REDCapDataModel
)

#
# REDCap Endpoints
#

@api.route("/<dm>", methods=["GET"])
class REDCapDataByDM(Resource):
    @api.doc("get_redcap_data_by_dm")
    @api.marshal_list_with(redcapDataModel)
    def get(self):
        """
        Get REDCap data pull by approved for Fairhub.io status
        """
        return REDCAP_DATA
