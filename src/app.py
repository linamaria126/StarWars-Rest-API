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
from models import db, User, People, Planets, Vehicles, Favorites, People_drive_vehicle
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

#Ruta para listar todos los Usuarios del blog
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    serialized_users = [user.serialize() for user in users]

    response_body = {
       "users": serialized_users
    },
      
    return jsonify(response_body), 200

#Ruta para listar todos los personajes
@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    serialized_people = [character.serialize() for character in people]

    response_body = {
       "people": serialized_people
    },
      
    return jsonify(response_body), 200

#Ruta para ver los detalles de un Personaje del blog
@app.route('/people/<int:people_uid>', methods=['GET'])
def get_people_uid(people_uid):
    character=People.query.filter_by(uid=people_uid).one_or_none()
    if character is None:
        return jsonify({"Error": "Character not found"}), 404
    return jsonify({"character": character.serialize()})


#Ruta para listar todos los Planetas
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    serialized_planets = [planet.serialize() for planet in planets]

    response_body = {
       "planets": serialized_planets
    },
      
    return jsonify(response_body), 200

#Ruta para ver los detalles de un Planeta
@app.route('/planet/<int:planet_uid>', methods=['GET'])
def get_planet_uid(planet_uid):
    planet=Planets.query.filter_by(uid=planet_uid).one_or_none()
    if planet is None:
        return jsonify({"Error": "Planet not found"}), 404
    return jsonify({"planet": planet.serialize()})

#Ruta para listar todos los vehículos
@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicles.query.all()
    serialized_vehicles = [vehicle.serialize() for vehicle in vehicles]

    response_body = {
       "vehicles": serialized_vehicles
    },
      
    return jsonify(response_body), 200

#Ruta para ver los detalles de un Vehículo
@app.route('/vehicle/<int:vehicle_uid>', methods=['GET'])
def get_vehicle_uid(vehicle_uid):
    vehicle=Vehicles.query.filter_by(uid=vehicle_uid).one_or_none()
    if vehicle is None:
        return jsonify({"Error": "Vehicle not found"}), 404
    return jsonify({"vehicle": vehicle.serialize()})


# this only runs if `$ python src/app.py` is executed

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
