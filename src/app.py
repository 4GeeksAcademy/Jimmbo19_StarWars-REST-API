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
from models import db, User,Planets,Characters
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
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
