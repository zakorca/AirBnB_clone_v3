#!/usr/bin/python3
"""
Create a view for Review objects that handles all default RESTFul API actions
"""
from flask import jsonify, abort, make_response, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def all_reviews(place_id):
    """ retreive list of all review objects of a place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    list_reviews = [review.to_dict() for review in place.reviews]
    return jsonify(list_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def review_id(review_id):
    """ retrieves a Review object indentified with id """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ delete a Review object and returns an empty dictionary """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """ creates a Review using POST method """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    if content.get("user_id") is None:
        abort(400, 'Missing user_id')

    user = storage.get(User, content['user_id'])
    if user is None:
        abort(404)

    if content.get("text") is None:
        abort(400, 'Missing text')

    content['place_id'] = place_id
    new_review = Review(**content)
    storage.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """ updates a Review object using PUT method """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if request.get_json() is None:
        abort(400, 'Not a JSON')
    content = request.get_json()

    list_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, val in content.items():
        if key not in list_keys:
            setattr(review, key, val)
    review.save()
    return make_response(jsonify(review.to_dict()), 200)
