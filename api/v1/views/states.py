#!/usr/bin/python3
"""
Create a view for State objects that handles all default RESTFul API actions
"""
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """ retrieve list of all state objects """
    states = storage.all(State).values()
    list_states = [state.to_dict() for state in states]
    return jsonify(list_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_id(state_id):
    """ retrieve a State object identified with id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ delete a state object and returns an empty dictionary """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ create state using POST method """
    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    if content.get("name") is None:
        abort(400, 'Missing name')
    new_st = State(**content)
    storage.save()
    return make_response(jsonify(new_st.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """ updtae a state object with id using PUT method """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.get_json() is None:
        abort(400, 'Not a JSON')
    content = request.get_json()
    list_keys = ['id', 'created_at', 'updated_at']
    for key, val in content.items():
        if key not in list_keys:
            setattr(state, key, val)
    state.save()
    return make_response(jsonify(state.to_dict()), 200)
