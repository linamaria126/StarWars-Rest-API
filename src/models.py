from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

    
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean, unique=False, nullable=False)
    favorites = db.relationship('Favorites', backref='user', lazy= True)

    def __repr__(self):
        return '<User %r>' % self.name
    
  
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
    uid = db.Column(db.Integer, primary_key=True)
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
    description = db.Column(db.Text, nullable=True)
    homeworldId = db.Column(db.Integer, db.ForeignKey('planets.uid'))
    people_drive_vehicle = db.relationship('People_drive_vehicle', backref='people')
    favorites = db.relationship('Favorites', backref='people', lazy= True)

    def __repr__(self):
        return '<People %r>' % self.name
    

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
            "description": self.description,
            "homeworldId": self.homeworldId,
            "people_drive_vehicles": self.people_drive_vehicle,
            "favorites": self.favorites
           
        }


class Vehicles(db.Model):
    __tablename__ = 'vehicles'
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    url = db.Column(db.String(250), nullable=False)
    model = db.Column(db.String(45), nullable=True)
    vehicle_class = db.Column(db.String(45), nullable=True)
    manufacturer = db.Column(db.String(45), nullable=True)
    length = db.Column(db.Float, nullable=True)
    crew = db.Column(db.Integer, nullable=True)
    max_atmosphering_speed = db.Column(db.Integer, nullable=True)
    cargo_capacity = db.Column(db.Integer, nullable=True)
    consumables = db.Column(db.String(45), nullable=True)
    created = db.Column(db.DateTime, nullable=True) #confirmar tipo de dato
    description = db.Column(db.Text, nullable=True)
    people_drive_vehicle = db.relationship("People_drive_vehicle", backref= 'vehicles')
    favorites = db.relationship("Favorites", backref= 'vehicles', lazy= True)

    def __repr__(self):
        return '<Vehicles %r>' % self.name
    

    def serialize(self):
        return{
            "uid": self.uid,
            "name": self.name,
            "url": self.url,
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "manufacturer": self.manufacturer,
            "length": self.length,
            "crew": self.crew,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "created": self.created,
            "description": self.description,
            "people_drive_vehicle": self.people_drive_vehicle,
            "favorites": self.favorites

        }

class Planets(db.Model):
    __tablename__ = 'planets'
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    url = db.Column(db.String(250), nullable=False)
    diameter = db.Column(db.Integer, nullable=True)
    rotation_period = db.Column(db.Integer, nullable=True)
    gravity = db.Column(db.Integer, nullable=True)
    climate = db.Column(db.String(45), nullable=True)
    terrain = db.Column(db.String(45), nullable=True)
    surface_water = db.Column(db.Integer, nullable=True)
    created = db.Column(db.DateTime, nullable=True) 
    description = db.Column(db.Text, nullable=True)
    favorites = db.relationship("Favorites", backref='planets', lazy= True )

    def __repr__(self):
        return '<Planets %r>' % self.name
    
    
    def serialize(self):
        return{
            "uid": self.uid,
            "name": self.name,
            "url": self.url,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "gravity": self.gravity,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "created" : self.created,
            "description": self.description,
            "favorites": self.favorites
        }


class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    people_uid = db.Column(db.Integer, db.ForeignKey('people.uid'), nullable=True)
    vehicles_uid = db.Column(db.Integer, db.ForeignKey('vehicles.uid'), nullable=True)
    planets_uid = db.Column(db.Integer, db.ForeignKey('planets.uid'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    def __repr__(self):
        return '<Favorites %r>' % self.id
    

    def serialize(self):
        people = db.query.get(self.people_uid)
        return{
            "id": self.id,
            "people_name": people.serialize()['name'],
            "vehicles_uid": self.vehicles_uid,
            "planets_uid": self.planets_uid,
            
        }


class People_drive_vehicle(db.Model):
    __tablename__ = 'people_drive_vehicles'
    people_drive_vehicles_id = db.Column(db.Integer, primary_key=True)
    people_uid = db.Column(db.Integer, db.ForeignKey('people.uid'))
    Vehicles_uid = db.Column(db.Integer, db.ForeignKey('vehicles.uid'))
    
    def __repr__(self):
        return '<People_drive_vehicle %r>' % self.name
    

    def serialize(self):
        return{
            "people_drive_vehicles_id": self.people_drive_vehicles_id,
            "people_uid": self.people_uid,
            "vehicles_uid": self.vehicles_uid,
            "vehicles": self.vehicles            
        }