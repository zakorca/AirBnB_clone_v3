#!/usr/bin/python3
"""
Create a view for the link between Place objects and Amenity objects
that handles all default RESTul API actions
"""
from flask import jsonify, abort, make_response, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views
import os


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def all_amenities_place(place_id):
    """ retrieve list of all amenity objects of a place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        list_amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        list_amenities = [storage.get(Amenity, amenity_id).to_dict()
                          for amenity_id in place.amenity_ids]
    return jsonify(list_amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_place(place_id, amenity_id):
    """delete an Amenity object to a Place and returns an empty dictionary"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)

    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_amenity_place(place_id, amenity_id):
    """ Link a Amenity object to a Place using POST method """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity in place.amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenity_ids.append(amenity)

    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
