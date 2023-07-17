"""Configuration for the application."""

import os
from dotenv import dotenv_values

FLASK_APP_DATABASE_URL = os.environ["FLASK_APP_DATABASE_URL"]

# take environment variables from .env
envcfg = dotenv_values(".env")

if "FLASK_APP_DATABASE_URL" in envcfg:
    FLASK_APP_DATABASE_URL = envcfg["FLASK_APP_DATABASE_URL"]

print(f"FLASK_APP_DATABASE_URL: {FLASK_APP_DATABASE_URL}")
