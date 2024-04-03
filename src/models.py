from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, Text, Float
from sqlalchemy.orm import relationship, declarative_base

db = SQLAlchemy()

    
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean, unique=False, nullable=False)
    favorites = db.relationship('Favorites', backref='user')
    
  
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "is_active": self.is_active,
            #"favorites": self.favorites
        }

class People(db.Model):
    __tablename__ = 'people'
    # Here we define db.Columns for the table person
    # Notice that each db.Column is also a normal Python instance attribute.
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    url = db.Column(db.String(250), nullable=False)
    height = db.Column(db.Integer, nullable=True)
    mass = db.Column(db.Integer, nullable=True)
    hair_color = db.Column(db.String(45), nullable=True)
    skin_color = db.Column(db.String(45), nullable=True)
    eye_color = db.Column(db.String(45), nullable=True)
    birth_year = db.Column(db.String(45), nullable=True)
    gender = db.Column(db.String(45), nullable=True)
    created = db.Column(db.DateTime, nullable=True) #confirmar tipo de dato
    edited = db.Column(db.DateTime, nullable=True) #confirmar tipo de dato
    description = db.Column(db.Text, nullable=True)
    _id = db.Column(db.Integer, nullable=True, autoincrement=True)
    _v = db.Column(db.Integer, nullable=True, autoincrement=True)
    homeworldId = db.Column(db.Integer, db.ForeignKey('planets.uid'))
    people_drive_vehicle = db.relationship('People_drive_vehicle', backref='people')
    favorites = db.relationship('Favorites', backref='people')

    def serialize(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "url": self.url,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "created": self.created,
            "edited": self.edited,
            "description": self.description,
            "_id": self._id,
            "_v": self._v,
            "homeworldId": self.homeworldId,
            "people_drive_vehicles": self.people_drive_vehicle,
            "favorites": self.favorites
           
        }


class Vehicles(db.Model):
    __tablename__ = 'vehicles'
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    url = db.Column(db.String(250), nullable=False)
    model = db.Column(db.String(45), nullable=True)
    vehicle_class = db.Column(db.String(45), nullable=True)
    manufacturer = db.Column(db.String(45), nullable=True)
    cost_in_credits = db.Column(db.Integer, nullable=True)
    length = db.Column(db.Float, nullable=True)
    crew = db.Column(db.Integer, nullable=True)
    max_atmosphering_speed = db.Column(db.Integer, nullable=True)
    cargo_capacity = db.Column(db.Integer, nullable=True)
    consumables = db.Column(db.String(45), nullable=True)
    created = db.Column(db.DateTime, nullable=True) #confirmar tipo de dato
    edited = db.Column(db.DateTime, nullable=True) #confirmar tipo de dato
    description = db.Column(db.Text, nullable=True)
    _id = db.Column(db.Integer, nullable=True)
    _v = db.Column(db.Integer, nullable=True)
    people_drive_vehicle = db.relationship("People_drive_vehicle", backref= 'vehicles')
    favorites = db.relationship("Favorites", backref= 'vehicles')

    def serialize(self):
        return{
            "uid": self.uid,
            "name": self.name,
            "url": self.url,
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "crew": self.crew,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "created": self.created,
            "edited": self.edited,
            "description": self.description,
            "_id": self._id,
            "_v": self._v,
            "people_drive_vehicle": self.people_drive_vehicle,
            "favorites": self.favorites

        }

class Planets(db.Model):
    __tablename__ = 'planets'
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    url = db.Column(db.String(250), nullable=False)
    diameter = db.Column(db.Integer, nullable=True)
    rotation_period = db.Column(db.Integer, nullable=True)
    manufacturer = db.Column(db.String(45), nullable=True)
    orbital_period = db.Column(db.Integer, nullable=True)
    length = db.Column(db.Float, nullable=True)
    gravity = db.Column(db.Integer, nullable=True)
    population = db.Column(db.Integer, nullable=True)
    climate = db.Column(db.String(45), nullable=True)
    terrain = db.Column(db.String(45), nullable=True)
    surface_water = db.Column(db.Integer, nullable=True)
    created = db.Column(db.DateTime, nullable=True) 
    edited = db.Column(db.DateTime, nullable=True) 
    description = db.Column(db.Text, nullable=True)
    _id = db.Column(db.Integer, nullable=True)
    _v = db.Column(db.Integer, nullable=True)
    favorites = db.relationship("Favorites", backref='planets' )
    
    def serialize(self):
        return{
            "uid": self.uid,
            "name": self.name,
            "url": self.url,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "manufacturer": self.manufacturer,
            "orbital_period": self.orbital_period,
            "length": self.length,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "created" : self.created,
            "edited": self.edited,
            "description": self.description,
            "_id": self._id,
            "_v": self._v,
            "favorites": self.favorites
        }


class Favorites(db.Model):
    __tablename__ = 'favorites'
    favorites_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    people_uid = db.Column(db.Integer, db.ForeignKey('people.uid'), nullable=True)
    vehicles_uid = db.Column(db.Integer, db.ForeignKey('vehicles.uid'), nullable=True)
    planets_uid = db.Column(db.Integer, db.ForeignKey('planets.uid'), nullable=True)
    user_uid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

  
    
    def serialize(self):
        return{
            "favorites_id": self.favorites_id,
            "people_uid": self.people_uid,
            "vehicles_uid": self.vehicles_uid,
            "planets_uid": self.planets_uid,
            "user_uid": self.user,
            #"people": {'name': self.people.name },
            #"vehicles": {'name': self.vehicles.name },
            #"planets": {'name': self.planets.name }
        }


class People_drive_vehicle(db.Model):
    __tablename__ = 'people_drive_vehicles'
    people_drive_vehicles_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    people_uid = db.Column(db.Integer, db.ForeignKey('people.uid'))
    Vehicles_uid = db.Column(db.Integer, db.ForeignKey('vehicles.uid'))
    
    

    def serialize(self):
        return{
            "people_drive_vehicles_id": self.people_drive_vehicles_id,
            "people_uid": self.people_uid,
            "vehicles_uid": self.vehicles_uid,
            "vehicles": self.vehicles            
        }