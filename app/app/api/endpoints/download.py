#!/usr/bin/python3
from flask import request, json
from ...core import downloads
from ...models import database as db_model
from ...main import app
from ...core import database as db_methods
from flask_cors import CORS, cross_origin
from ...models import user as user_model
from ...models import store as store_model

cors = CORS(app)


@cross_origin("http://localhost")
@app.route("/api/updatedownloads/", methods=["POST"])
def update_downloads():
    """
    Update the download counter for the current time
    :return: a normal post request status code and message explaining the status code
    """
    username = request.json.get('username')
    song_name = request.json.get('songname')
    user = user_model.User(username)
    db = db_model.MusicDbModel()
    local_store_model = store_model.WooModel("LOCAL")
    global_store_model = store_model.WooModel("GLOBAL")
    download_methods = downloads.DownloadsAPI()
    result = download_methods.update_downloads(username, song_name, db, global_store_model, local_store_model)
    if result == -1:
        response = app.response_class(
            response=json.dumps("could not write to db"),
            status=400,
            mimetype="application/json"
        )
        return response
    elif not isinstance(result, str) and result >= 0:
        response = app.response_class(
            response=json.dumps(result),
            status=200,
            mimetype="application/json"
        )
        return response
    else:
        response = app.response_class(
            response=json.dumps("It has been less than 30 minutes since the last update"),
            status=200,
            mimetype="application/json"
        )
        return response


@cross_origin("http://localhost")
@app.route("/api/initiatedownload/", methods=["POST"])
def initiate_download_counter():
    song_name = request.json.get('songname')
    username = request.json.get('username')
    local_id = request.json.get('localID')
    aws_id = request.json.get('awsID')
    db = db_model.MusicDbModel()
    db_methods_object = db_methods.MusicShareDbAPI()
    response_from_db = db_methods_object.initiate_download(db, song_name, username, local_id, aws_id)
    if response_from_db:
        response = app.response_class(
            response=json.dumps("data written to db"),
            status=200, mimetype="application/json"
        )
    else:
        response = app.response_class(
            response=json.dumps("could not write to the db"),
            status=400,
            mimetype="application/json"
        )
    return response
