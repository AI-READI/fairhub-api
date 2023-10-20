import os
from flask_restx import Api

# Import API Namespaces
from .root import api as root
from .redcap import api as redcap

# from .caching import api as caching
from .dashboard import api as dashboard

# Init API
api = Api(
    title=os.environ["FLASK_APP_TITLE"],
    version=os.environ["FLASK_APP_VERSION"],
    description=os.environ["FLASK_APP_SUMMARY"],
)

# Register API Namespaces
api.add_namespace(root)
api.add_namespace(redcap)
api.add_namespace(dashboard)
# api.add_namespace(caching)
