#!/usr/bin/python3
from flask import Flask

app = Flask(__name__)
# Setup app
from core import app_setup  # noqa

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host="0.0.0.0", debug=True, port=5000)

