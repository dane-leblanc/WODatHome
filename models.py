from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to db"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Users"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    
    workouts = db.relationship('Workout', backref='user', cascade='all, delete')
    
    @classmethod
    def register(cls, username, password):
        """register user with hashed password and return User"""
        
        hashed = bcrypt.generate_password_hash(password)
        #turn bytestsring into normal string
        hashed_utf8 = hashed.decode('utf8')
        
        #return instance of all user attributes with hashed password
        return cls(username=username, password=hashed_utf8)
    
    @classmethod
    def authenticate(cls, username, password):
        """Validate that a user exists & password is correct.
        Return user if valid, else return False."""
        
        u = User.query.filter_by(username=username).first()
        
        if u and bcrypt.check_password_hash(u.password, password):
            return u
        else:
            return False
    
class Workout(db.Model):
    """Workouts"""
    __tablename__ = 'workouts'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    exercises = db.Column(db.PickleType, nullable=False)
    
    #I'm unsure if I want results to be deleted if the workout is deleted. 
    results = db.relationship('Result', backref='workout', cascade='all, delete')
    
class Result(db.Model):
    """Workout results"""
    ___tablename__ = 'results'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow())
    note = db.Column(db.String(100))
    
class Exercise(db.Model):
    """Exercise Data from WGER API"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category_id = db.Column(db.Integer)