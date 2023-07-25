from flask import Flask
from flask_cors import CORS
from pyfairdatatools import __version__
from flask_restx import Api, Resource, reqparse

import model
from apis.dataset import dataset
from apis.participant import participant
from apis.study import study
from apis.contributor import contributor
from core import config

app = Flask(__name__)
app.config.from_prefixed_env("FAIRHUB")


if "DATABASE_URL" in app.config:
    print("DATABASE_URL: ", app.config["DATABASE_URL"])
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config["DATABASE_URL"]
else:
    print("FAIRHUB_DATABASE_URL: ", config.FAIRHUB_DATABASE_URL)
    app.config["SQLALCHEMY_DATABASE_URI"] = config.FAIRHUB_DATABASE_URL

api = Api(
    app,
    title="FAIRHUB",
    description="The backend api system for the Vue app",
    doc="/docs",
)


fhb = api.namespace("fairhub", description="FAIRhub tools")


model.db.init_app(app)
app.register_blueprint(study)
app.register_blueprint(dataset)
app.register_blueprint(participant)
app.register_blueprint(contributor)


CORS(app)


@app.cli.command("create-schema")
def create_schema():
    model.db.create_all()


@app.route("/", methods=["GET"])
class Home(Resource):
    def home(self):
        return "Home page"


if __name__ == "__main__":
    app.run(debug=True)
