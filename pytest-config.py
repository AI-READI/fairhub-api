"""Configuration for the application."""
from os import environ

FAIRHUB_DATABASE_URL = environ.get("FAIRHUB_DATABASE_URL")
FAIRHUB_SECRET = environ.get("secret")
TESTING = True
print("####################")
print(FAIRHUB_DATABASE_URL)
print(FAIRHUB_SECRET)
print("TESTING EXISTS: ", "TESTING" in environ)
print("####################")
