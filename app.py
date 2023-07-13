import os, toml, dotenv

# Load API Metadata from .env
dotenv.load_dotenv()

# Load API Metadata from pyproject.toml
pyproject_metadata = toml.load("pyproject.toml")
os.environ["FLASK_APP_NAME"] = pyproject_metadata["tool"]["poetry"]["name"]
os.environ["FLASK_APP_VERSION"] = pyproject_metadata["tool"]["poetry"]["version"]
os.environ["FLASK_APP_DESCRIPTION"] = pyproject_metadata["tool"]["poetry"]["description"]
os.environ["FLASK_APP_LICENSE"] = pyproject_metadata["tool"]["poetry"]["license"]

from flask import Flask
from flask_cors import CORS
from flask_restx import Api

from apis.root import api as root
from apis.redcap import api as redcap
from apis.dashboards import api as dashboards

# Init API
api = Api(
    title=os.environ["FLASK_APP_TITLE"],
    version=os.environ["FLASK_APP_VERSION"],
    description=os.environ["FLASK_APP_SUMMARY"],
)

# Register Namespaces
api.add_namespace(root)
api.add_namespace(redcap)
api.add_namespace(dashboards)

# Init Flask
app = Flask(__name__)
api.init_app(app)
CORS(app)

# from apis import getStudies, updateStudies, participants

# db = SQLAlchemy(app)
# app.config.from_object('fairdata.default_settings')
# app.config.from_envvar('FAIRDATA_SETTINGS')

# db.init_app(app)

import redis

# Init Redis Cache
cache = redis.Redis(
    host=os.environ["REDIS_CACHE_HOST"],
    port=os.environ["REDIS_CACHE_PORT"],
    username=os.environ["REDIS_CACHE_USERNAME"],
    password=os.environ["REDIS_CACHE_PASSWORD"],
    decode_responses=True
)

if __name__ == "__main__":

    # Default to port 5000 if FLASK_PORT isn't specified in .flaskenv
    # this gets around an issue on MacOS where port 5000 is used by
    # the OS and allowing Flask to use it causes a Heisenbug (in this
    # case a silent, intermittent failure with no clear pattern)
    FLASK_PORT = os.environ["FLASK_PORT"] if "FLASK_PORT" in os.environ else 5000
    FLASK_DEBUG = os.environ["FLASK_DEBUG"] if "FLASK_DEBUG" in os.environ else False
    app.run(debug=True, port=FLASK_PORT)
else:
    pass
