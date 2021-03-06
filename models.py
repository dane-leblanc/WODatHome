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

    workouts = db.relationship(
        'Workout', backref='user', cascade='all, delete')
    results = db.relationship(
        'Result', backref='user', cascade='all, delete')

    @classmethod
    def register(cls, username, password):
        """register user with hashed password and return User"""

        hashed = bcrypt.generate_password_hash(password)
        # turn bytestsring into normal string
        hashed_utf8 = hashed.decode('utf8')

        # create User with hashed password
        user = User(
            username=username,
            password=hashed_utf8)

        db.session.add(user)

        return user

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
    name = db.Column(db.String, nullable=False)
    stages = db.Column(db.Integer)
    stage_time = db.Column(db.Integer)

    results = db.relationship(
        'Result', backref='workout', cascade='all, delete')

    workout_exercises = db.relationship(
        'WorkoutExercise', backref='workout', cascade='all, delete')

    def serialize(self):
        """Returns a dict representation of Workout to turn to JSON"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type,
            'name': self.name,
            'stages': self.stages,
            'stage_time': self.stage_time
        }


class Result(db.Model):
    """Workout results"""
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    workout_id = db.Column(
        db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow())
    note = db.Column(db.String(100))


class Category(db.Model):
    """Category Data from WGER API"""
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)

    exercises = db.relationship('Exercise', backref='category')


class Exercise(db.Model):
    """Exercise Data from WGER API"""
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    category_id = db.Column(
        db.Integer, db.ForeignKey('categories.id'), nullable=False)

    equipment = db.relationship(
        'Equipment', secondary='exercises_equipment', backref='exercises')

    exercise_workouts = db.relationship('WorkoutExercise', backref='exercise')


class Equipment(db.Model):
    """Equipment Data from WGER API"""
    __tablename__ = 'equipment'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)


class ExerciseEquipment(db.Model):
    """Mapping of Exercise to Equipment"""
    __tablename__ = 'exercises_equipment'

    exercise_id = db.Column(
        db.Integer, db.ForeignKey('exercises.id'), primary_key=True)
    equipment_id = db.Column(
        db.Integer, db.ForeignKey('equipment.id'), primary_key=True)


class WorkoutExercise(db.Model):
    """Details of exercises stored with a workout"""
    __tablename__ = 'workouts_exercises'

    workout_id = db.Column(
        db.Integer, db.ForeignKey('workouts.id'), primary_key=True)
    order = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(
        db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    count = db.Column(db.Integer)
    count_type = db.Column(db.String(10))


class ExerciseImage(db.Model):
    """Exercise Image from WGER API"""
    __tablename__ = 'exercise_images'

    exercise_id = db.Column(
        db.Integer,
        db.ForeignKey('exercises.id'),
        primary_key=True)
    image_url = db.Column(db.String, nullable=False)
