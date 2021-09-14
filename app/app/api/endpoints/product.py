#!/usr/bin/python3
from flask import request, json
from core import downloads
from models import database as db_model
from main import app
from core import database as db_methods
from core import product as prod_methods
from flask_cors import CORS, cross_origin
from models import user as user_model
from models import store as store_model

cors = CORS(app)


@cross_origin("http://localhost")
@app.route('/api/create-product/', methods=['POST'])
def create_product():
    """
    Add a product to the global and local store
    :return: a normal post request status code and message explaining the status code
    """
    global_file_path = request.json.get('global_file_path')
    local_file_path = request.json.get('local_file_path')
    file_names = request.json.get('file_names')
    db_model_object = db_model.MusicDbModel()
    local_store_model = store_model.WooModel("LOCAL")
    global_store_model = store_model.WooModel("GLOBAL")
    prod_methods_object = prod_methods.ProductAPI()
    result = prod_methods_object.create_product_entry(global_store_model, local_store_model, db_model_object,
                                                      global_file_path, local_file_path, file_names)
    if result:
        confirmation = {
            "message": "product created"
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
            "message": "product failed to be added"
        }
        response = app.response_class(
            response=json.dumps(error),
            status=400,
            mimetype="application/json"
        )
        db_model_object.close_connection()
        return response  # automatically jsonify'd
