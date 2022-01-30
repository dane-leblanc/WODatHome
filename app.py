from flask import Flask, render_template, redirect, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Workout, Result, Category, Exercise, Equipment, ExerciseEquipment, WorkoutExercise, ExerciseImage
from forms import UserAddForm, LoginForm, SearchExerciseForm
import os
import re
import fetch

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

@app.route('/browse', methods=["GET", "POST"])
def browse():
    form = SearchExerciseForm()
    if form.validate_on_submit():
        print('validated on submit')
        name_input = form.name.data
        category_input = form.category.data
        equipment_id_input = form.equipment.data
        exercises = []
        
        # automatically include "none" and "gym mat" to equipment list
        equip_list = [Equipment.query.get(7), Equipment.query.get(4)]
        for id in equipment_id_input:
            equip_list.append(Equipment.query.get(int(id)))
        
        # if user did not select a category, do not include a category in the exercise filter
        if category_input != '<none>':
            cat = Category.query.filter_by(name=category_input).one()
        
            all_exercises = Exercise.query.filter(Exercise.name.ilike(f'%{name_input}%'), Exercise.category_id == cat.id).all()
            
        else: 
            all_exercises = Exercise.query.filter(Exercise.name.ilike(f'%{name_input}%')).all()

        # Check the equipment needed for each exercise against the equipment the user marked as 'available'. Remove any exercises that require equipment beyond what's available.
        for exercise in all_exercises:
            if set(exercise.equipment).issubset(set(equip_list)) == True:
                exercises.append(exercise)
        
        return render_template('browse.html', form=form, exercises=exercises)
        
    return render_template('browse.html', form=form)

@app.route('/users/<username>')
def user_home(username):
    if 'username' not in session or username != session['username']:
        return redirect('/')
    else:
        user = User.query.filter_by(username=username).one()
        return render_template('user_home.html', user=user)
        
    
@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')