from flask import Flask
from flask_cors import CORS
from pyfairdatatools import __version__

import model
from apis.dataset import dataset
from apis.participant import participant
from apis.study import study

from core import config

app = Flask(__name__)
app.config.from_prefixed_env("FAIRDATA")
app.config["SQLALCHEMY_DATABASE_URI"] = config.FLASK_APP_DATABASE_URL


model.db.init_app(app)
app.register_blueprint(study)
app.register_blueprint(dataset)
app.register_blueprint(participant)

CORS(app)

print(__version__)


@app.cli.command("create-schema")
def echo():
    model.db.create_all()


@app.route("/", methods=["GET"])
def home():
    return "Home page"


if __name__ == "__main__":
    app.run(debug=True)
