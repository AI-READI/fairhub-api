from flask import Flask
from flask_cors import CORS
from pyfairdatatools import __version__
from flask_restx import Api, Resource, reqparse


import model
from apis.dataset import dataset
from apis.participant import participant
from apis.study import study

from core import config

app = Flask(__name__)
app.config.from_prefixed_env("FAIRHUB")


if "DATABASE_URL" in app.config:
    print("DATABASE_URL: ", app.config["DATABASE_URL"])
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config["DATABASE_URL"]
else:
    print("FAIRHUB_DATABASE_URL: ", config.FAIRHUB_DATABASE_URL)
    app.config["SQLALCHEMY_DATABASE_URI"] = config.FAIRHUB_DATABASE_URL


model.db.init_app(app)
app.register_blueprint(study)
app.register_blueprint(dataset)
app.register_blueprint(participant)

CORS(app)

print(__version__)


@app.cli.command("create-schema")
def create_schema():
    model.db.create_all()


@app.route("/", methods=["GET"])
def home():
    return "Home page"


if __name__ == "__main__":
    app.run(debug=True)
