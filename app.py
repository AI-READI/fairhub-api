from flask import Flask
from flask_cors import CORS

from apis.getStudies import bp
from apis.participants import participants_bp
app = Flask(__name__)

app.register_blueprint(bp)
CORS(app)


# from apis import getStudies, updateStudies, participants
# db = SQLAlchemy(app)
# app.config.from_object('fairdata.default_settings')
# app.config.from_envvar('FAIRDATA_SETTINGS')

# db.init_app(app)


if __name__ == "__main__":
    app.run(debug=True)
