"""Configuration for the application."""

import os
from dotenv import dotenv_values

FLASK_APP_DATABASE_URL = os.environ.get("FLASK_APP_DATABASE_URL")

# take environment variables from .env.local
envcfg = dotenv_values(".env.local")

if "FLASK_APP_DATABASE_URL" in envcfg:
    FLASK_APP_DATABASE_URL = envcfg["FLASK_APP_DATABASE_URL"]
