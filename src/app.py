"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, abort
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Starship, Weapon
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    return jsonify([c.serialize() for c in characters])

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Character.query.get(character_id)
    if not character:
        abort(404, description="Character not found")
    return jsonify(character.serialize())

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([p.serialize() for p in planets])

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        abort(404, description="Planet not found")
    return jsonify(planet.serialize())

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([u.serialize() for u in users])

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404, description="User not found")

    favorites = {
        "planets": [planet.serialize() for planet in user.favorite_planets],
        "characters": [character.serialize() for character in user.favorite_characters],
        "starships": [starship.serialize() for starship in user.favorite_starships],
        "weapons": [weapon.serialize() for weapon in user.favorite_weapons]
    }
    return jsonify(favorites)

@app.route('/users/<int:user_id>/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(user_id, planet_id):
    user = User.query.get(user_id)
    planet = Planet.query.get(planet_id)

    if not user or not planet:
        abort(404, description="User or Planet not found")

    if planet in user.favorite_planets:
        return jsonify({"message": "Planet already in favorites"}), 200

    user.favorite_planets.append(planet)
    db.session.commit()

    return jsonify({"message": f"Planet '{planet.name}' added to user {user.email}'s favorites"}), 201

@app.route('/users/<int:user_id>/favorite/planet/<int:planet_id>', methods=['DELETE'])
def remove_favorite_planet(user_id, planet_id):
    user = User.query.get(user_id)
    planet = Planet.query.get(planet_id)

    if not user or not planet:
        abort(404, description="User or Planet not found")

    user.favorite_planets.remove(planet)
    db.session.commit()

    return jsonify({"message": f"Planet '{planet.name}' removed from user {user.email}'s favorites"}), 201

@app.route('/users/<int:user_id>/favorite/character/<int:character_id>', methods=['POST'])
def add_favorite_character(user_id, character_id):
    user = User.query.get(user_id)
    character = Character.query.get(character_id)

    if not user or not character:
        abort(404, description="User or Character not found")

    if character in user.favorite_characters:
        return jsonify({"message": "Character already in favorites"}), 200

    user.favorite_characters.append(character)
    db.session.commit()

    return jsonify({"message": f"Character '{character.name}' added to user {user.email}'s favorites"}), 201

@app.route('/users/<int:user_id>/favorite/character/<int:character_id>', methods=['DELETE'])
def remove_favorite_character(user_id, character_id):
    user = User.query.get(user_id)
    character = Character.query.get(character_id)

    if not user or not character:
        abort(404, description="User or Character not found")

    user.favorite_characters.remove(character)
    db.session.commit()

    return jsonify({"message": f"Character '{character.name}' removed from user {user.email}'s favorites"}), 201

@app.route('/users/<int:user_id>/favorite/starship/<int:starship_id>', methods=['POST'])
def add_favorite_starship(user_id, starship_id):
    user = User.query.get(user_id)
    starship = Starship.query.get(starship_id)

    if not user or not starship:
        abort(404, description="User or Starship not found")

    if starship in user.favorite_starships:
        return jsonify({"message": "Starship already in favorites"}), 200

    user.favorite_starships.append(starship)
    db.session.commit()

    return jsonify({"message": f"Starship '{starship.name}' added to user {user.email}'s favorites"}), 201

@app.route('/users/<int:user_id>/favorite/starship/<int:starship_id>', methods=['DELETE'])
def remove_favorite_starship(user_id, starship_id):
    user = User.query.get(user_id)
    starship = Starship.query.get(starship_id)

    if not user or not starship:
        abort(404, description="User or Starship not found")

    user.favorite_starships.remove(starship)
    db.session.commit()

    return jsonify({"message": f"Starship'{starship.name}' removed from user {user.email}'s favorites"}), 201


@app.route('/users/<int:user_id>/favorite/weapon/<int:weapon_id>', methods=['POST'])
def add_favorite_weapon(user_id, weapon_id):
    user = User.query.get(user_id)
    weapon = Weapon.query.get(weapon_id)

    if not user or not weapon:
        abort(404, description="User or Weapon not found")

    if weapon in user.favorite_weapons:
        return jsonify({"message": "Weapon already in favorites"}), 200

    user.favorite_weapons.append(weapon)
    db.session.commit()

    return jsonify({"message": f"Weapon '{weapon.name}' added to user {user.email}'s favorites"}), 201

@app.route('/users/<int:user_id>/favorite/weapon/<int:weapon_id>', methods=['DELETE'])
def remove_favorite_weapon(user_id, weapon_id):
    user = User.query.get(user_id)
    weapon = Weapon.query.get(weapon_id)

    if not user or not weapon:
        abort(404, description="User or weapon not found")

    user.favorite_weapons.remove(weapon)
    db.session.commit()

    return jsonify({"message": f"Weapon'{weapon.name}' removed from user {user.email}'s favorites"}), 201
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
