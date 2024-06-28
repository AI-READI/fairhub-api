"""Entry point for the application."""

import datetime
import importlib
import logging
import os
from datetime import timezone

import click
import jwt
from flask import Flask, g, request
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from growthbook import GrowthBook
from sqlalchemy import MetaData, inspect, text
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.schema import DropTable
from waitress import serve

import caching
import config
import model
from apis import api
from apis.authentication import UnauthenticatedException, authentication, authorization
from apis.exception import ValidationException

# from pyfairdatatools import __version__

bcrypt = Bcrypt()


# Add Cascade to Table Drop Call in destroy-schema CLI command
@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler):
    return f"{compiler.visit_drop_table(element)} CASCADE"


def create_app(config_module=None, loglevel="INFO"):
    """Initialize the core application."""
    # create and configure the app
    app = Flask(__name__)
    # `full` if you want to see all the details
    app.config["SWAGGER_UI_DOC_EXPANSION"] = "none"
    app.config["RESTX_MASK_SWAGGER"] = False

    # set up logging
    logging.basicConfig(level=getattr(logging, loglevel))

    # Initialize config
    app.config.from_object(config_module or "config")

    # app.register_blueprint(api)
    # TODO - fix this
    # csrf = CSRFProtect()
    # csrf.init_app(app)

    if config.FAIRHUB_SECRET:
        if len(config.FAIRHUB_SECRET) < 32:
            raise RuntimeError("FAIRHUB_SECRET must be at least 32 characters long")
    else:
        raise RuntimeError("FAIRHUB_SECRET not set")

    if config.FAIRHUB_DATABASE_URL:
        # if "TESTING" in app_config and app_config["TESTING"]:
        #     pass
        # else:
        #   print("DATABASE_URL: ", app.config["DATABASE_URL"])
        # app.config["SQLALCHEMY_DATABASE_URI"] = app.config["DATABASE_URL"]
        app.config["SQLALCHEMY_DATABASE_URI"] = config.FAIRHUB_DATABASE_URL
    else:
        # throw error
        raise RuntimeError("FAIRHUB_DATABASE_URL not set")

    model.db.init_app(app)
    api.init_app(app)
    bcrypt.init_app(app)
    caching.cache.init_app(app)

    cors_origins = [
        "https://brave-ground-.*-.*.centralus.2.azurestaticapps.net",  # noqa E501 # pylint: disable=line-too-long # pylint: disable=anomalous-backslash-in-string
        "https://staging.app.fairhub.io",
        "https://app.fairhub.io",
        "https://staging.fairhub.io",
        "https://fairhub.io",
    ]
    if app.debug:
        cors_origins.extend(["http://localhost:3000"])

    # Only allow CORS origin for localhost:3000
    # and any subdomain of azurestaticapps.net/
    CORS(
        app,
        resources={
            "/*": {
                "origins": cors_origins,
            }
        },
        allow_headers=[
            "Content-Type",
            "Authorization",
            "Access-Control-Allow-Origin",
            "Access-Control-Allow-Credentials",
        ],
        supports_credentials=True,
    )

    # app.config[
    #     "CORS_ALLOW_HEADERS"
    # ] = "Content-Type, Authorization, Access-Control-Allow-Origin, Access-Control-Allow-Credentials"
    # app.config[
    #     "CORS_EXPOSE_HEADERS"
    # ] = "Content-Type, Authorization, Access-Control-Allow-Origin, Access-Control-Allow-Credentials"
    # app.config["CORS_SUPPORTS_CREDENTIALS"] = True

    # CORS(app, resources={r"/*": {"origins": "*", "send_wildcard": True}})

    @app.cli.command("create-schema")
    def create_schema():
        """Create the database schema."""
        engine = model.db.session.get_bind()
        metadata = MetaData()
        metadata.reflect(bind=engine)
        table_names = [table.name for table in metadata.tables.values()]
        if len(table_names) == 0:
            with engine.begin():
                model.db.create_all()

    @app.cli.command("destroy-schema")
    def destroy_schema():
        """Create the database schema."""
        # If DB is Azure, Skip
        if config.FAIRHUB_DATABASE_URL.find("azure") > -1:
            return
        engine = model.db.session.get_bind()
        with engine.begin() as conn:
            model.db.drop_all()
            # conn.execute(text("DROP TABLE IF EXISTS alembic_version"))

    @app.cli.command("cycle-schema")
    def cycle_schema():
        """Destroy then re-create the database schema."""
        # If DB is Azure, Skip
        if config.FAIRHUB_DATABASE_URL.find("azure") > -1:
            return
        engine = model.db.session.get_bind()
        metadata = MetaData()
        metadata.reflect(bind=engine)
        table_names = [table.name for table in metadata.tables.values()]
        if len(table_names) == 0:
            with engine.begin():
                model.db.drop_all()
                model.db.create_all()

    @app.cli.command("list-schemas")
    def list_schemas():
        engine = model.db.session.get_bind()
        inspector = inspect(engine)
        schema_names = inspector.get_schema_names()
        print("SCHEMAS")
        for schema_name in schema_names:
            print(schema_name)

    @app.cli.command("inspect-schema")
    @click.argument("schema")
    def inspect_schema(schema=None):
        """Print database schemas, tables, and columns to CLI.
        Optional argument schema. Default all schemas inspected.
        """
        engine = model.db.session.get_bind()
        inspector = inspect(engine)
        schema_names = inspector.get_schema_names()
        for schema_name in schema_names:
            if schema is None or schema == schema_name:
                print("-" * 38)
                print(f"SCHEMA: {schema_name}")
                print("-" * 38)
                for table_name in inspector.get_table_names(schema=schema_name):
                    print(f"  Table: {table_name}")
                    for column in inspector.get_columns(table_name, schema=schema_name):
                        print(f"    Column: {column['name']}")
                        for k, v in column.items():
                            print(f"      {k:<16}{str(v):>16}")
                    print("\n ", "-" * 36)

    @app.before_request
    def on_before_request():  # pylint: disable = inconsistent-return-statements
        if request.method == "OPTIONS":
            return

        try:
            authentication()

            authorization()

            # create growthbook instance
            g.gb = GrowthBook(
                api_host="https://cdn.growthbook.io",
                client_key=config.FAIRHUB_GROWTHBOOK_CLIENT_KEY,
            )

            # load feature flags
            g.gb.load_features()

        except UnauthenticatedException:
            return "Authentication is required", 401

    @app.after_request
    def on_after_request(resp):
        # destroy growthbook instance
        if hasattr(g, "gb"):
            g.gb.destroy()

        public_routes = [
            "/auth",
            "/docs",
            "/echo",
            "/swaggerui",
            "/swagger.json",
            "/favicon.ico",
        ]
        for route in public_routes:
            if request.path.startswith(route):
                return resp

        if "token" not in request.cookies:
            return resp

        token: str = request.cookies.get("token") or ""  # type: ignore

        # Determine the appropriate configuration module based on the testing context
        if os.environ.get("FLASK_ENV") == "testing":
            config_module_name = "pytest_config"
        else:
            config_module_name = "config"
        config_module = importlib.import_module(config_module_name)
        if os.environ.get("FLASK_ENV") == "testing":
            # If testing, use the 'TestConfig' class for accessing 'secret'
            config = config_module.TestConfig
        else:
            # If not testing, directly use the 'config' module
            config = config_module
        try:
            decoded = jwt.decode(token, config.FAIRHUB_SECRET, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            resp.set_cookie(
                "token",
                "",
                secure=True,
                httponly=True,
                samesite="None",
                expires=datetime.datetime.now(timezone.utc),
            )
            return resp
        token_blacklist = model.TokenBlacklist.query.get(decoded["jti"])
        if token_blacklist:
            resp.delete_cookie("token")
            return resp
        expired_in = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
            minutes=180
        )

        new_token = jwt.encode(
            {"user": decoded["user"], "exp": expired_in, "session": decoded["session"], "jti": decoded["jti"]},
            config.FAIRHUB_SECRET,
            algorithm="HS256",
        )
        resp.set_cookie("token", new_token, secure=True, httponly=True, samesite="None")

        app.logger.info("after request")
        app.logger.info(request.headers.get("Origin"))

        resp.headers["Access-Control-Allow-Origin"] = request.headers.get("Origin")
        resp.headers["Access-Control-Allow-Credentials"] = "true"
        # resp.headers[
        #     "Access-Control-Allow-Headers"
        # ] = "Content-Type, Authorization, Access-Control-Allow-Origin,
        # Access-Control-Allow-Credentials"
        # resp.headers[
        #     "Access-Control-Expose-Headers"
        # ] = "Content-Type, Authorization, Access-Control-Allow-Origin,
        # Access-Control-Allow-Credentials"
        app.logger.info(resp.headers)
        return resp

    @app.errorhandler(ValidationException)
    def validation_exception_handler(error):
        return error.args[0], 422

    with app.app_context():
        engine = model.db.session.get_bind()
        metadata = MetaData()
        metadata.reflect(bind=engine)
        table_names = [table.name for table in metadata.tables.values()]

        # The alembic table is created by default, so we need to check for more than 1 table
        if len(table_names) <= 1:
            with engine.begin():
                model.db.create_all()

    return app


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        "-P", "--port", default=5000, type=int, help="Port to listen on"
    )
    parser.add_argument("-H", "--host", default="0.0.0.0", type=str, help="Host")
    parser.add_argument(
        "-L", "--loglevel", default="INFO", type=str, help="Logging level"
    )
    args = parser.parse_args()
    port = args.port
    host = args.host
    loglevel = args.loglevel

    flask_app = create_app(loglevel=loglevel)

    serve(flask_app, port=port, host=host)
