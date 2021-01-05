from flask import jsonify
from ...core import auth
from flask import request, json
from ...models import user as user_model
from ...models import database as db_model
from ...main import app
from ...core import database as db_methods
from ...core import auth
from flask_cors import CORS, cross_origin
from ...models import user as user_model
from ...core import coupon
from ...models import store as store_model

cors = CORS(app)


@cross_origin("http://localhost")
@app.route("/api/create-coupon", methods=['POST'])
def create_coupon():
    """ Creates a coupon
    :return: a normal post request status code and message explaining the status code
    """
    username = request.json.get('username')
    password = request.json.get('password')
    song_name = request.json.get('songname')
    db_model_object = db_model.MusicDbModel()
    db_methods_class = db_methods.MusicShareDbAPI()
    user = user_model.User(username)
    # retrieve hashed password from db
    user.password_hash = db_methods_class.get_user_password(db_model_object, username)
    # check to see if db connection failed
    if user.password_hash == -1:
        error = {
            "message": "cannot connect to the db"
        }
        response = app.response_class(
            response=json.dumps(error),
            status=400,
            mimetype="application/json"
        )
        db_model_object.close_connection()
        return response  # automatically jsonify'd
    # check for missing arguments
    if len(username) == 0 or len(password) == 0:
        error = {
            "message": "username or pin was empty"
        }
        response = app.response_class(
            response=json.dumps(error),
            status=400,
            mimetype="application/json"
        )
        db_model_object.close_connection()
        return response  # automatically jsonify'd
    # check to see if the user is in the db
    is_user = db_methods_class.check_for_user(db_model_object, username)
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
        return response  # automatically jsonify'd
    # check password
    auth_object = auth.MusicShareAPIAuth()
    auth_object.hash_password(user, password)
    valid_password = auth_object.verify_password(password, user.password_hash)
    coupon_methods = coupon.CouponAPI()
    local_store_model = store_model.WooModel("LOCAL")
    global_store_model = store_model.WooModel("GLOBAL")
    if is_user and valid_password:
        coupon_response_local = coupon_methods.create(local_store_model, song_name, user.username, -1)
        coupon_response_aws = ""
        if len(coupon_response_local) == 10:
            coupon_response_aws = create_coupon.create(global_store_model, song_name, username, coupon_response_local)
        if len(coupon_response_local) != 10 and len(coupon_response_aws) != 10:  # if its not a coupon code
            error = {
                "message": "Coupon could not be created"
            }
            response = app.response_class(
                response=json.dumps(error),
                status=400,
                mimetype="application/json"
            )
            db_model_object.close_connection()
            return response  # automatically jsonify'd
        else:
            confirmation = {
                "message": coupon_response_local
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
            "message": "username or pin is incorrect"
        }
        response = app.response_class(
            response=json.dumps(error),
            status=400,
            mimetype="application/json"
        )
        db_model_object.close_connection()
        return response  # automatically jsonify'd
