from flask import Flask
import model
from flask_cors import CORS
from apis.study import study
from apis.dataset import dataset
from apis.participant import participant
from pyfairdatatools import __version__


app = Flask(__name__)
app.config.from_prefixed_env("FAIRDATA")
app.config["SQLALCHEMY_DATABASE_URI"] = app.config["DATABASE_URL"]


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
