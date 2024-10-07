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
    
class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User)

    favorite_type = db.Column(db.String(50), nullable=False)  # Either 'planet' or 'character'
     
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=True)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=True)
    planet = db.relationship(Planets)
    character = db.relationship(Characters)

    def __repr__(self):
        return f'<Favorites user_id={self.user_id}, type={self.favorite_type}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "favorite_type": self.favorite_type,
            "planet_id": self.planet_id,
            "character_id": self.character_id,
        }
