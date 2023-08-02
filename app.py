"""Entry point for the application."""
import os
import logging

from flask import Flask
from flask_cors import CORS

import model
from apis import api
from core import config

# from pyfairdatatools import __version__


def create_app(app_config):
    """Initialize the core application."""
    app = Flask(__name__)

    SECRET_KEY = os.urandom(32)
    app.config["SECRET_KEY"] = SECRET_KEY

    # full if you want to see all the details
    app.config.SWAGGER_UI_DOC_EXPANSION = "list"

    app.logger.setLevel(logging.DEBUG)

    # print(config)
    # print(app_config)

    # TODO - fix this
    # csrf = CSRFProtect()
    # csrf.init_app(app)

    app.config.from_prefixed_env("FAIRHUB")

    if "DATABASE_URL" in app.config:
        # if "TESTING" in app_config and app_config["TESTING"]:
        #     pass
        # else:
        #     print("DATABASE_URL: ", app.config["DATABASE_URL"])
        app.config["SQLALCHEMY_DATABASE_URI"] = app.config["DATABASE_URL"]
    else:
        # if "TESTING" in app_config and app_config["TESTING"]:
        #     pass
        # else:
        # print("FAIRHUB_DATABASE_URL: ", config.FAIRHUB_DATABASE_URL)
        app.config["SQLALCHEMY_DATABASE_URI"] = config.FAIRHUB_DATABASE_URL

    model.db.init_app(app)
    api.init_app(app)

    CORS(app, resources={r"/*": {"origins": "*", "send_wildcard": "True"}})

    @app.cli.command("create-schema")
    def create_schema():
        """Create the database schema."""
        model.db.create_all()

    #
    # @api.route("/")
    # @api.doc(responses={404: "not found"})
    # class Home(Resource):
    #     def home(self):
    #         return "Home page"
    #

    return app


if __name__ == "__main__":
    flask_app = create_app(config)
    flask_app.run(debug=True)
