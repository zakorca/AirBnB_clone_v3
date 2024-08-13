#!/usr/bin/python3
"""
Create a view for Place objects that handles all default RESTul API actions
"""
from flask import jsonify, abort, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def all_places(city_id):
    """ retrieve list of all place objects of a city """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    list_places = [place.to_dict() for place in city.places]
    return jsonify(list_places)


@app_views.route('places/<place_id>', methods=['GET'], strict_slashes=False)
def place_id(place_id):
    """ retrieves a Place object identified with id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ delete a place object and returns an empty dictionary """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """ creates a place using POST method """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    if content.get("user_id") is None:
        abort(400, 'Missing user_id')

    user = storage.get(User, content['user_id'])
    if user is None:
        abort(404)

    if content.get("name") is None:
        abort(400, 'Missing name')

    content['city_id'] = city_id
    new_place = Place(**content)
    storage.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """ updates a place object using PUT method """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.get_json() is None:
        abort(400, 'Not a JSON')
    content = request.get_json()
    list_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, val in content.items():
        if key not in list_keys:
            setattr(place, key, val)
    place.save()
    return make_response(jsonify(place.to_dict()), 200)
