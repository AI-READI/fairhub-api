# Environment imports
import dotenv
import toml
import os
import json

#
# Define Globals
#

global DASHBOARD_CONFIG
global MEMORY_CACHE

#
# Load Environment
#

# Load API metadata from .env
dotenv.load_dotenv()

# Load API metadata from pyproject.toml
pyproject_toml = toml.load("pyproject.toml")
os.environ["FLASK_APP_NAME"] = pyproject_toml["tool"]["poetry"]["name"]
os.environ["FLASK_APP_VERSION"] = pyproject_toml["tool"]["poetry"]["version"]
os.environ["FLASK_APP_DESCRIPTION"] = pyproject_toml["tool"]["poetry"]["description"]
os.environ["FLASK_APP_LICENSE"] = pyproject_toml["tool"]["poetry"]["license"]

# Load JSON config files
with open("config/dashboards.json") as config:
    DASHBOARDS_CONFIG = json.load(config)

#
# Setup Cache
#

# Cache imports
from flask_caching import Cache

MEMORY_CACHE = Cache(
    config={
        "CACHE_TYPE": "RedisCache",
        "CACHE_DEFAULT_TIMEOUT": os.environ["CACHE_DEFAULT_TIMEOUT"],
        "CACHE_KEY_PREFIX": os.environ["CACHE_KEY_PREFIX"],
        "CACHE_REDIS_HOST": os.environ["CACHE_REDIS_HOST"],
        "CACHE_REDIS_PORT": os.environ["CACHE_REDIS_PORT"],
        "CACHE_REDIS_DB": os.environ["CACHE_REDIS_DB"],
        "CACHE_REDIS_URL": os.environ["CACHE_REDIS_URL"],
    }
)

#
# Initialize Flask
#

# Flask API imports
from flask import Flask
from flask_cors import CORS
from apis import api

app = Flask(__name__)
api.init_app(app)
MEMORY_CACHE.init_app(app)
CORS(app)

# from apis import getStudies, updateStudies, participants

# db = SQLAlchemy(app)
# app.config.from_object('fairdata.default_settings')
# app.config.from_envvar('FAIRDATA_SETTINGS')

# db.init_app(app)

if __name__ == "__main__":
    # Default to port 5000 if FLASK_PORT isn't specified in .flaskenv
    # Using a different port gets around an issue on MacOS where port
    # 5000 is used by and the OS and Flask, which leads to a Heisenbug
    FLASK_PORT = os.environ["FLASK_PORT"] if "FLASK_PORT" in os.environ else 5000
    FLASK_DEBUG = os.environ["FLASK_DEBUG"] if "FLASK_DEBUG" in os.environ else False
    app.run(debug=True, port=FLASK_PORT)
else:
    pass
