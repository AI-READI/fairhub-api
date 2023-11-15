#!/bin/sh

alembic upgrade head

python app.py
