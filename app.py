from flask import Flask
from flask_cors import CORS

import model
from apis import api
from core import config

# from pyfairdatatools import __version__


app = Flask(__name__)

app.config.from_prefixed_env("FAIRHUB")

if "DATABASE_URL" in app.config:
    print("DATABASE_URL: ", app.config["DATABASE_URL"])
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config["DATABASE_URL"]
else:
    print("FAIRHUB_DATABASE_URL: ", config.FAIRHUB_DATABASE_URL)
    app.config["SQLALCHEMY_DATABASE_URI"] = config.FAIRHUB_DATABASE_URL


model.db.init_app(app)
api.init_app(app)

CORS(app)


@app.cli.command("create-schema")
def create_schema():
    model.db.create_all()


#
# @api.route("/")
# @api.doc(responses={404: "not found"})
# class Home(Resource):
#     def home(self):
#         return "Home page"
#


if __name__ == "__main__":
    app.run(debug=True)
