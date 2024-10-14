"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User,Planets,Characters,Favorites
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

@app.route('/user', methods=['GET'])
def handle_hello():

    all_users= User.query.all()
    results_users= list(map(lambda usuario: usuario.serialize() ,all_users))

    return jsonify(results_users), 200

@app.route('/planets', methods=['GET'])
def get_planets():

    all_planets= Planets.query.all()
    results_planets= list(map(lambda planetas: planetas.serialize() ,all_planets))

    return jsonify(results_planets), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):

    planet= Planets.query.filter_by(id=planet_id).first()
    

    return jsonify(planet.serialize()), 200

@app.route('/characters', methods=['GET'])
def get_characters():

    all_characters= Characters.query.all()
    results_characters= list(map(lambda personajes: personajes.serialize() ,all_characters))

    return jsonify(results_characters), 200

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):

    character= Characters.query.filter_by(id=character_id).first()
    

    return jsonify(character.serialize()), 200

@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
  
    favorites = db.session.query(
        User.email, 
        Favorites.favorite_type, 
        Planets.name.label('planet_name'), 
        Characters.name.label('character_name')
    ).join(Favorites, User.id == Favorites.user_id) \
    .outerjoin(Planets, Favorites.planet_id == Planets.id) \
    .outerjoin(Characters, Favorites.character_id == Characters.id) \
    .filter(User.id == user_id).all()

   
    result = []
    for fav in favorites:
        if fav.favorite_type == 'planet':
            result.append({
                "user": fav.email,
                "favorite": fav.planet_name,
                "type": "planet"
                
                
            })
        elif fav.favorite_type == 'character':
            result.append({
                "user": fav.email,
                "favorite": fav.character_name,
                "type": "character"
                
                
            })
    
    return jsonify(result)

@app.route('/planets', methods=['POST'])
def post_planet():
    body=request.get_json()
    planeta = Planets(**body)
    db.session.add(planeta)
    db.session.commit()
    return jsonify(planeta.serialize()), 201

@app.route('/characters', methods=['POST'])
def post_characters():
    body=request.get_json()
    personaje = Characters(**body)
    db.session.add(personaje)
    db.session.commit()
    return jsonify(personaje.serialize()), 201

@app.route('/user/<int:user_id>/favorites', methods=['POST'])
def add_favorite(user_id):
    body = request.get_json()

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    favorite_type = body.get('favorite_type')
    favorite_id = body.get('favorite_id')

    if not favorite_type or not favorite_id:
        return jsonify({"error": "Missing favorite_type or favorite_id"}), 400

 
    if favorite_type == 'planet':
        planet = Planets.query.get(favorite_id)
        if not planet:
            return jsonify({"error": "Planet not found"}), 404

        new_favorite = Favorites(user_id=user_id, favorite_type='planet', planet_id=favorite_id)

    elif favorite_type == 'character':
        character = Characters.query.get(favorite_id)
        if not character:
            return jsonify({"error": "Character not found"}), 404

        new_favorite = Favorites(user_id=user_id, favorite_type='character', character_id=favorite_id)

    else:
        return jsonify({"error": "Invalid favorite_type"}), 400


    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({"message": "Favorite added successfully", "favorite": new_favorite.serialize()}), 201


@app.route('/characters/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):

    character= Characters.query.filter_by(id=character_id).first()
    db.session.delete(character)
    db.session.commit()

    return jsonify({"message": "Character deleted"}), 200

@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):

    planet= Planets.query.filter_by(id=planet_id).first()
    db.session.delete(planet)
    db.session.commit()

    return jsonify({"message": "Planet deleted"}), 200
        

@app.route('/user/<int:user_id>/favorites/<int:favorite_id>', methods=['DELETE'])
def delete_favorite(user_id, favorite_id):
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

   
    favorite = Favorites.query.filter_by(id=favorite_id, user_id=user_id).first()
    if not favorite:
        return jsonify({"error": "Favorite not found"}), 404

    
    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": "Favorite deleted successfully"}), 200
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
