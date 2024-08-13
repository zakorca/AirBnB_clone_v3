#!/usr/bin/python3
""" Flask app that intercats with html """
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close(excep):
    """ close sqlalchemy session """
    storage.close()


@app.errorhandler(404)
def not_found(err):
    """ return not found page in json format """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    """ main flask app """
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
