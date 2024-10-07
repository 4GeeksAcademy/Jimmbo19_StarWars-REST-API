from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "activo":self.is_active,
        }
    
class Planets(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    terrain = db.Column(db.String(250), nullable=False)
    population = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
             "id": self.id,
             "name": self.name,
             "terrain":self.terrain,
           
            }

class Characters(db.Model):
   
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250), nullable=False)
    height = db.Column(db.String(250), nullable=False)
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    planets = db.relationship('Planets')
 
    def __repr__(self):
        return '<Characters %r>' % self.name

    def serialize(self):
        return {
             "id": self.id,
             "name": self.name,
             "height":self.height,
             "planet":self.planets_id,
            
            }
    
class UserPlanetsFavorites(db.Model):
    

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    planets = db.relationship(Planets)
    def __repr__(self):
        return '<UserPlanetsFavorites %r>' % self.User

    def serialize(self):
        return {
             "id": self.id,
             "user": self.user_id,
             "planet":self.planets_id,
            
            }
    
class UserCharactersFavorites(db.Model):
    

    id =db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)
    characters_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    characters = db.relationship(Characters)
    def __repr__(self):
        return '<UserCharactersFavorites %r>' % self.User

    def serialize(self):
        return {
             "id": self.id,
             "user": self.user_id,
             "character":self.characters_id,
            
            }