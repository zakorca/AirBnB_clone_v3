#!/usr/bin/python3
"""
Create a view for Amenity objects that handles all default RESTFul API actions
"""
from flask import jsonify, abort, make_response, request
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """ retrieve list af all amenity objects """
    amenities = storage.all(Amenity).values()
    list_amenities = [amenity.to_dict() for amenity in amenities]
    return jsonify(list_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenity_id(amenity_id):
    """ retrieve an Amenity object identified with id """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ delete an amenity object and returns an empty dictionary """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """ creates an amenity using POST method """
    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    if content.get("name") is None:
        abort(400, 'Missing name')
    new_amenity = Amenity(**content)
    storage.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """ update an amenity object with id using PUT method """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if request.get_json() is None:
        abort(400, 'Not a JSON')
    content = request.get_json()
    list_keys = ['id', 'created_at', 'updated_at']
    for key, val in content.items():
        if key not in list_keys:
            setattr(amenity, key, val)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 200)
