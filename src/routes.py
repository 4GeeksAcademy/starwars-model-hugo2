from flask import Flask, request, jsonify, Blueprint
from src.models import db, User, Character, Planet, Favourite

api = Blueprint('api', __name__)


def get_current_user():
    """
    Como todavía no hay autenticación, usamos el primer usuario de la base de datos
    como usuario actual.
    """
    return User.query.first()


@api.route('/people', methods=['GET'])
def get_people():
    people = Character.query.all()
    return jsonify({
        "message": "ok",
        "results": [person.serialize() for person in people]
    }), 200


@api.route('/people/<int:people_id>', methods=['GET'])
def get_single_person(people_id):
    person = Character.query.get(people_id)

    if person is None:
        return jsonify({"message": "Person not found"}), 404

    return jsonify({
        "message": "ok",
        "result": person.serialize()
    }), 200


@api.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify({
        "message": "ok",
        "results": [planet.serialize() for planet in planets]
    }), 200


@api.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    planet = Planet.query.get(planet_id)

    if planet is None:
        return jsonify({"message": "Planet not found"}), 404

    return jsonify({
        "message": "ok",
        "result": planet.serialize()
    }), 200


@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify({
        "message": "ok",
        "results": [user.serialize() for user in users]
    }), 200


@api.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    current_user = get_current_user()

    if current_user is None:
        return jsonify({"message": "No users found in database"}), 404

    return jsonify({
        "message": "ok",
        "results": [favorite.serialize() for favorite in current_user.favourites]
    }), 200


@api.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    current_user = get_current_user()

    if current_user is None:
        return jsonify({"message": "No users found in database"}), 404

    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"message": "Planet not found"}), 404

    existing_favorite = Favourite.query.filter_by(
        user_id=current_user.id,
        planet_id=planet_id
    ).first()

    if existing_favorite:
        return jsonify({"message": "Planet already in favorites"}), 400

    favorite = Favourite(user_id=current_user.id, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({
        "message": "Favorite planet added successfully",
        "result": favorite.serialize()
    }), 201


@api.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_person(people_id):
    current_user = get_current_user()

    if current_user is None:
        return jsonify({"message": "No users found in database"}), 404

    person = Character.query.get(people_id)
    if person is None:
        return jsonify({"message": "Person not found"}), 404

    existing_favorite = Favourite.query.filter_by(
        user_id=current_user.id,
        character_id=people_id
    ).first()

    if existing_favorite:
        return jsonify({"message": "Person already in favorites"}), 400

    favorite = Favourite(user_id=current_user.id, character_id=people_id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({
        "message": "Favorite person added successfully",
        "result": favorite.serialize()
    }), 201


@api.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    current_user = get_current_user()

    if current_user is None:
        return jsonify({"message": "No users found in database"}), 404

    favorite = Favourite.query.filter_by(
        user_id=current_user.id,
        planet_id=planet_id
    ).first()

    if favorite is None:
        return jsonify({"message": "Favorite planet not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": "Favorite planet deleted successfully"}), 200


@api.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_person(people_id):
    current_user = get_current_user()

    if current_user is None:
        return jsonify({"message": "No users found in database"}), 404

    favorite = Favourite.query.filter_by(
        user_id=current_user.id,
        character_id=people_id
    ).first()

    if favorite is None:
        return jsonify({"message": "Favorite person not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": "Favorite person deleted successfully"}), 200
