from flask import Flask, request, json
from flask_cors import CORS, cross_origin
from .core import app_setup

app = Flask(__name__)


def main():
    hello()


@app.route("/")
def hello():
    return "Hello World from Flask in a uWSGI Nginx Docker container with \
     Python 3.8 from iNethi Music Share"


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host="0.0.0.0", debug=True, port=80)
