from flask import Flask
from flask_cors import CORS
from apis import api
app = Flask(__name__)
api.init_app(app)
from apis import getStudies, updateStudies, addParticipants

CORS(app)
app.secret_key = "fairhub_key"


if __name__ == "__main__":
    app.run(debug=True)
