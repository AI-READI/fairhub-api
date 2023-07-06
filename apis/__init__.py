from flask_restx import Api

from .root import api as root

api = Api(
    title="fairhub.io API",
    version="0.1",
    description="Data storage, access and retrieval API for fairhub.io",
)


api.add_namespace(root)

# Another way of doing it:
# api.add_namespace(ns2, path='/prefix/of/ns2')
