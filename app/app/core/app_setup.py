#!/usr/bin/python3
from api import api  # noqa
from main import app


@app.route("/hello/")
def hello():
    # This could also be returning an index.html
    return """Hello World from Flask in a uWSGI Nginx Docker container with Python 3.8"""
