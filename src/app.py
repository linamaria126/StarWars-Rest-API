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
from models import db, User, People, Planets, Vehicles, Favorites
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


#Ruta para crear un favorito de la lista de people, con el people_id.
@app.route('/favorite/people/<int:people_uid>', methods=['POST'])
def post_people_uid(people_uid):

    body = request.json
    user_uid = body.get('user_uid', None )
    
    new_people_favorite = Favorites(people_uid = people_uid, user_id = user_uid)
    db.session.add(new_people_favorite)
    try:     
                 
        db.session.commit()
        return jsonify({"msg":"People Favorite created", "id": new_people_favorite.id }), 201
    
    except Exception as error:
        db.session.rollback()
        print(error)
        return jsonify({"error":str(error)}), 500
    
#Ruta para crear un favorito de la lista de planets, con el planet_id.
@app.route('/favorite/planet/<int:planet_uid>', methods=['POST'])
def post_planet_uid(planet_uid):

    body = request.json
        
    user_uid = body.get('user_uid', None )
    new_planet_favorite = Favorites(planets_uid = planet_uid, user_id = user_uid)
    db.session.add(new_planet_favorite)

    try:
        db.session.commit()
        return jsonify({"msg":"Planet Favorite created", "id": new_planet_favorite.id }), 201
    
    except Exception as error:
        db.session.rollback()
        print(error)
        return jsonify('There is a problem'), 500
    

# Ruta para mostrar todos los favoritos de un usuario  
@app.route('/favorite/<int:user_uid>', methods=['GET'])
def get_favorite_byUser(user_uid):

    favorites = Favorites.query.filter_by(user_uid=user_uid)
    serialized_favorites = [favorite.serialize() for favorite in favorites]
     

    print(serialized_favorites)
    return jsonify({'results': serialized_favorites}), 200

# Ruta para mostrar todos los favoritos de people con su respectivo nombre
@app.route('/favorite', methods=['GET'])
def get_favorite():

    #favorites = Favorites.query.all()
    #favorites = db.session.query(Favorites, People, Planets, User).join(People,Favorites.people_uid==People.uid).join(Planets,Favorites.planets_uid==Planets.uid).join(User, Favorites.user_id==User.id).all()
    #serialized_favorites = [favorite.serialize() for favorite in favorites]
    #favorites = db.session.query(Favorites, People,Planets).join(People, Favorites.people_uid==People.uid).join(Planets, Favorites.planets_uid==Planets.uid).all()
    favorites = db.session.query(Favorites, People).join(People, Favorites.people_uid==People.uid).all()
    serialized_favorites = list(map(lambda fav:{
        "idfavorito": fav[0].id,
        "idpeople": fav[1].uid,
        "namepeople": fav[1].name,
        #"user_id": fav[2].user_id,
        #"idplanets": fav[2].uid,
        #"nameplanets": fav[2].name,
    }, favorites))
     

    print(serialized_favorites)
    return jsonify({'results': serialized_favorites}), 200


#Ruta para borrar un 'people' favorito
@app.route('/favorite/people/<int:people_uid>', methods=['DELETE'])
def delete_people_uid(people_uid):

    body = request.json
    user_uid = body.get('user_uid', None )
    
    delete_people_favorite = Favorites.query.filter_by(people_uid = people_uid, user_id = user_uid).one_or_none()
    db.session.delete(delete_people_favorite)
    try:     
                 
        db.session.commit()
        return jsonify({"msg":"Favorite deleted", "id": delete_people_favorite.id}), 201
    
    except Exception as error:
        db.session.rollback()
        print(error)
        return jsonify({"error":str(error)}), 500


#Ruta para borrar un 'planet' favorito
@app.route('/favorite/planet/<int:planet_uid>', methods=['DELETE'])
def delete_planet_uid(planet_uid):

    body = request.json
    user_uid = body.get('user_uid', None )
    
    delete_planet_favorite = Favorites.query.filter_by(planets_uid = planet_uid, user_id = user_uid).first()
    db.session.delete(delete_planet_favorite)
    try:     
                 
        db.session.commit()
        return jsonify({"msg":"Favorite deleted", "id": delete_planet_favorite.id}), 201
    
    except Exception as error:
        db.session.rollback()
        print(error)
        return jsonify({"error":str(error)}), 500


# this only runs if `$ python src/app.py` is executed

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
