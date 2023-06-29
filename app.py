from flask import Flask

from flask_cors import CORS
from apis import api
from flask import jsonify
import random

app = Flask(__name__)
api.init_app(app)
CORS(app)

from apis import getStudies, updateStudies, participants

# db = SQLAlchemy(app)

# app.config.from_object('fairdata.default_settings')
# app.config.from_envvar('FAIRDATA_SETTINGS')

# db.init_app(app)


if __name__ == "__main__":
    app.run(debug=True)
