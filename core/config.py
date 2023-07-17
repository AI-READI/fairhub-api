"""Configuration for the application."""

from dotenv import dotenv_values

FLASK_APP_DATABASE_URL = "sqlite:///./app.db"

# take environment variables from .env.local
envcfg = dotenv_values(".env.local")

if "FLASK_APP_DATABASE_URL" in envcfg:
    FLASK_APP_DATABASE_URL = envcfg["FLASK_APP_DATABASE_URL"]
