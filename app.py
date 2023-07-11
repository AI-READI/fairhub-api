from flask import Flask
from model import *
from flask_cors import CORS
from apis.study import study
from apis.dataset import dataset
from apis.participant import participant

import click

app = Flask(__name__)
app.config.from_prefixed_env("FAIRDATA")
app.config["SQLALCHEMY_DATABASE_URI"] = app.config["DATABASE_URL"]


db.init_app(app)
app.register_blueprint(study)
app.register_blueprint(dataset)
app.register_blueprint(participant)

CORS(app)


@app.cli.command("echo")
@click.argument("message")
def echo(message):
    print(message)


@app.cli.command("create-schema")
def echo():
    db.create_all()


@app.route("/", methods=["GET"])
def home():
    return 'Home page'


if __name__ == "__main__":
    app.run(debug=True)
