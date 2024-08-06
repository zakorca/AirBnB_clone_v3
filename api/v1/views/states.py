#!/usr/bin/python3
""" States_RestFul API actions """
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """ return list of all_states """
    list_objs = []
    for i in storage.all('State').values():
        list_objs.append(i.to_dict())
    return jsonify(list_objs)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_one_obj(state_id):
    """ return 1 obj by id """
    obj = storage.get('State', str(state_id))
    if obj is None:
        abort(404)
    if obj is not None:
        return jsonify(obj.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_obj(state_id):
    """ delete state obj """
    obj = storage.get('State', state_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_obj():
    """ create state obj """
    old = request.get_json(silent=True)
    if old is None:
        abort(400, description="Not a JSON")
    if 'name' not in old:
        abort(400, description="Missing name")
    new_obj = State(**old)
    new_obj.save()
    return jsonify(new_obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_obj(state_id):
    """ update state obj """
    old = request.get_json(silent=True)
    if old is None:
        abort(400, description="Not a JSON")
    obj = storage.get('State', state_id)
    if obj is None:
        abort(404)
    ignore_list = ['id', 'created_at', 'updated_at']
    for i, j in old.items():
        if i not in ignore_list:
            setattr(obj, i, j)
    obj.save()
    return jsonify(obj.to_dict()), 200
