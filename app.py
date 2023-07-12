import dotenv; dotenv.load_dotenv()

import os, redis

from flask import Flask
from flask_cors import CORS

from apis import api

# Load Environment Variables

# Init Flask
app = Flask(__name__)
api.init_app(app)
CORS(app)


# from apis import getStudies, updateStudies, participants

# db = SQLAlchemy(app)
# app.config.from_object('fairdata.default_settings')
# app.config.from_envvar('FAIRDATA_SETTINGS')

# db.init_app(app)

# Init Redis Cache
cache = redis.Redis(
    host=os.environ["REDIS_CACHE_HOST"],
    port=os.environ["REDIS_CACHE_PORT"],
    username=os.environ["REDIS_CACHE_USERNAME"],
    password=os.environ["REDIS_CACHE_PASSWORD"],
    decode_responses=True
)

if __name__ == "__main__":
    app.run(debug=True, port=os.environ["FLASK_PORT"] if "FLASK_PORT" in os.environ else 5000)
else:
    pass
