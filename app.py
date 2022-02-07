from flask import Flask, render_template, redirect, jsonify, session, request
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Workout, Result, Category, Exercise, Equipment, ExerciseEquipment, WorkoutExercise, ExerciseImage
from forms import UserAddForm, LoginForm, SearchExerciseForm, AddWorkoutForm
import os
import re
import fetch
import queries

from secret import API_SECRET_KEY

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///WODatHome_db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = "SECRET WORKOUT!!!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def root():
    if "username" not in session:
        return redirect('/home')
    else:
        username = session['username']
        return redirect(f'/users/{username}')
    

@app.route('/home')
def home_page():
    if "username" in session:
        return redirect('/')
    else:
        return render_template('home.html')


@app.route('/register', methods=["GET", "POST"])
def register_user():
    if "username" in session:
        return redirect('/')
    form = UserAddForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        new_user = User.register(username, password)
        db.session.commit()
        session['username'] = new_user.username
        return redirect(f'/users/{new_user.username}')
    
    return render_template("register.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.authenticate(username, password)
        if user:
            session['username'] = username
            return redirect(f'/users/{username}')
        else:
            form.username.errors = ['Username/Password not found. Please try again.']
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route('/browse', methods=["GET"])
def browse():
    form = SearchExerciseForm(request.args)

    name_input = request.args.get("name")
    category_input = request.args.get("category")
    equipment_id_input = request.args.getlist("equipment")
    
    if category_input:
        equip_list = queries.get_equip_list(equipment_id_input)
        
        exercises = queries.get_exercises(equip_list, name_input, category_input)
        
        return render_template('browse.html', form=form, exercises=exercises, equip_list=equip_list)

    return render_template('browse.html', form=form)    


@app.route('/exercise/<int:id>')
def exercise_details(id):
    e = Exercise.query.get(id)
    e_img = queries.get_exercise_image(id)
    
    return render_template('exercise_details.html', e=e, e_img=e_img)


@app.route('/users/<username>')
def user_home(username):
    if 'username' not in session or username != session['username']:
        return redirect('/')
    else:
        user = User.query.filter_by(username=username).one()
        workouts = Workout.query.filter_by(user_id=user.id).all()
        return render_template('user_home.html', user=user, workouts=workouts)


@app.route('/users/<username>/workout/<int:id>')
def workout_info(username, id):
    """Show the exercises within this workout and give options to delete and execute workout"""
    if 'username' not in session or username != session['username']:
        return redirect('/')
    else:
        workout = Workout.query.get(id)
        exercises = WorkoutExercise.query.filter_by(workout_id=workout.id).all()
        if workout.type == 'AMRAP':
            exercises_per_stage = int((len(exercises) - workout.stages + 1) / workout.stages)
            workout_stages = []
            tick = 0
            while tick < len(exercises):
                workout_stages.append(exercises[tick:tick+exercises_per_stage])
                tick = tick + exercises_per_stage + 1
            rest_time = exercises[exercises_per_stage].count
            return render_template('workout_details.html', workout=workout, exercises=exercises, username=username, workout_stages=workout_stages, rest_time=rest_time)


@app.route('/users/<username>/workout/<int:id>/delete', methods=["POST"])
def delete_workout(username, id):
    if 'username' not in session or username != session['username']:
        return redirect('/')
    else:
        workout = Workout.query.get(id)
        db.session.delete(workout)
        db.session.commit()
        return redirect(f'/users/{username}')


@app.route('/users/<username>/workout/create', methods=["GET", "POST"])
def create_workout(username):
    """Create an empty workout (no exercises). Don't commit to db until exercises are associated with the workout."""
    if 'username' not in session or username != session['username']:
        return redirect('/')
    else:
        db.session.rollback()
        user = User.query.filter_by(username=username).one()
        form = AddWorkoutForm()
        if form.validate_on_submit():
            type = form.type.data
            name = form.name.data

            new_workout = Workout(
                user_id=user.id,
                type=type,
                name=name
            )
            db.session.add(new_workout)
            return redirect(f'/users/{username}/workout/create/{new_workout.name}')

        return render_template("create_workout.html", form=form, user=user)


@app.route('/users/<username>/workout/create/<workout_name>', methods=["GET", "POST"])
def add_workout_exercises(username, workout_name):
    if 'username' not in session or username != session['username']:
        return redirect('/')
    else:
        browse_form = SearchExerciseForm(request.args)

        name_input = request.args.get("name")
        category_input = request.args.get("category")
        equipment_id_input = request.args.getlist("equipment")
    
        if category_input:
            equip_list = queries.get_equip_list(equipment_id_input)
        
            exercises = queries.get_exercises(equip_list, name_input, category_input)
        
            return render_template('add_workout_exercises.html', browse_form=browse_form, exercises=exercises, equip_list=equip_list, username=username, workout_name=workout_name)

        return render_template('add_workout_exercises.html', username=username, workout_name=workout_name, browse_form=browse_form)
        
    
@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')


"""RESTFUL API for AJAX requests"""
@app.route('/api/exercises/<int:id>')
def get_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    return jsonify(exercise=exercise.serialize())