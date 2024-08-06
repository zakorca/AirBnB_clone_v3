#!/usr/bin/python3
"""
Create a view for City objects that handles all default RESTul API actions
"""
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def all_cities(state_id):
    """ retrieve list of all city objects of a state """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    list_cities = [city.to_dict() for city in state.cities]
    return jsonify(list_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_id(city_id):
    """ retrieve a City object identified with id """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ delete a city object and returns an empty dictionary """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """ create city using POST method """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    if content.get("name") is None:
        abort(400, 'Missing name')
    new_city = City(**content)
    new_city.state_id = state.id
    storage.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """ update a city object using PUT method """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.get_json() is None:
        abort(400, 'Not a JSON')
    content = request.get_json()
    list_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, val in content.items():
        if key not in list_keys:
            setattr(city, key, val)
    city.save()
    return make_response(jsonify(city.to_dict()), 200)
