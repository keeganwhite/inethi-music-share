#!/usr/bin/python3
from flask import request, json
from models import user as user_model
from models import database as db_model
from main import app
from core import database as db_methods
from core import auth
from flask_cors import CORS, cross_origin


cors = CORS(app)


@app.route("/test/", methods=['GET'])
def test():
    message = {
        "message": "hello from user.py endpoint"
    }
    response = app.response_class(
        response=json.dumps(message),
        status=200,
        mimetype="application/json"
    )
    # db_model_object.close_connection()
    return response  # automatically jsonify'd


@cross_origin("http://localhost")
@app.route('/api/newuser/', methods=['POST'])
def new_user():
    """
    Add a new user to the DB
    :return: a normal post request status code and message explaining the status code
    """

    username = request.json.get('username')
    password = request.json.get('password')
    user = user_model.User(username)
    if len(username) == 0 or len(password) == 0:
        error = {
            "message": "username or pin was empty"
        }
        response = app.response_class(
            response=json.dumps(error),
            status=400,
            mimetype="application/json"
        )
        # db_model_object.close_connection()
        return response  # automatically jsonify'd
    # check if user exists
    db_model_object = db_model.MusicDbModel()
    db_methods_class = db_methods.MusicShareDbAPI()
    is_user = db_methods_class.check_for_user(db_model_object, user.username)
    if is_user == -1:
        error = {
            "message": "cannot connect to the db"
        }
        response = app.response_class(
            response=json.dumps(error),
            status=400,
            mimetype="application/json"
        )
        db_model_object.close_connection()
        return response
    elif is_user:
        error = {
            "message": "username exists already"
        }
        response = app.response_class(
            response=json.dumps(error),
            status=400,
            mimetype="application/json"
        )
        db_model_object.close_connection()
        return response  # automatically jsonify'd

    auth_object = auth.MusicShareAPIAuth()
    result = db_methods_class.add_user(db_model_object, username, auth_object.password_hash(user, password))
    # check if user was successfully added to the database
    if result:
        confirmation = {
            "message": "user has been added to the database"
        }
        response = app.response_class(
            response=json.dumps(confirmation),
            status=200,
            mimetype="application/json"
        )
        db_model_object.close_connection()
        return response  # automatically jsonify'd
    else:
        error = {
            "message": "user could not be added to the database at this time"
        }
        response = app.response_class(
            response=json.dumps(error),
            status=400,
            mimetype="application/json"
        )
        db_model_object.close_connection()
        return response  # automatically jsonify'd
