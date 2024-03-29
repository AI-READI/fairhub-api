"""Entry point for the application."""
import os

from flask import Flask
from flask_cors import CORS

import model
from apis import api


# from pyfairdatatools import __version__


def create_app():
    """Initialize the core application."""
    # create and configure the app
    app = Flask(__name__)

    # `full` if you want to see all the details
    app.config.SWAGGER_UI_DOC_EXPANSION = "list"

    # Initialize config
    app.config.from_pyfile("config.py")
    # app.register_blueprint(api)

    # TODO - fix this
    # csrf = CSRFProtect()
    # csrf.init_app(app)

    app.config.from_prefixed_env("FAIRHUB")

    # print(app.config)

    if "DATABASE_URL" in app.config:
        # if "TESTING" in app_config and app_config["TESTING"]:
        #     pass
        # else:
        #   print("DATABASE_URL: ", app.config["DATABASE_URL"])
        app.config["SQLALCHEMY_DATABASE_URI"] = app.config["DATABASE_URL"]
    else:
        # throw error
        raise RuntimeError("FAIRHUB_DATABASE_URL not set")

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
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        "-p", "--port", default=5000, type=int, help="port to listen on"
    )
    args = parser.parse_args()
    port = args.port

    app = create_app()

    app.run(host="0.0.0.0", port=port)
