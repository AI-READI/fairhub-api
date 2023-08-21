from flask import request
from flask_restx import Namespace, Resource, fields


api = Namespace("study", description="study operations", path="/")
