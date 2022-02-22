"""Use these functions to fill our database with data from wger API"""
import requests
import os
import re
from models import (
    db,
    Category,
    Exercise,
    Equipment,
    ExerciseImage,
    ExerciseEquipment,
    WorkoutExercise,
    User,
    Workout)
from app import app

# from secret import API_SECRET_KEY, sample_password

API_KEY = os.environ.get('WGER_API_KEY')

API_BASE_URL = 'https://wger.de/api/v2/'

headers = {
    "Authorization": f"Token {API_KEY}",
    "Accept": "application/json; indent=4"}


def fill_categories():
    """Fill categories table with external API data"""

    response = requests.get(f"{API_BASE_URL}exercisecategory", headers=headers)

    res_json = response.json()
    results = res_json['results']

    for result in results:
        new_category = Category(id=result['id'], name=result['name'])
        db.session.add(new_category)

    rest = Category(id=1, name='Rest')
    db.session.add(rest)

    db.session.commit()

    return "Categories Table Filled"


def fill_equipment():
    """Fill equipment table with external API data"""
    response = requests.get(f"{API_BASE_URL}equipment", headers=headers)

    res_json = response.json()
    results = res_json['results']

    for result in results:
        new_equipment = Equipment(id=result['id'], name=result['name'])
        db.session.add(new_equipment)

    db.session.commit()

    return "Equipment Table Filled"


def fill_exercises():
    """Fill exercises table with external API data."""
    response = requests.get(
        f"{API_BASE_URL}/exercise/?language=2&limit=231", headers=headers)

    res_json = response.json()
    results = res_json['results']

    for result in results:
        new_exercise = Exercise(
            id=result['id'],
            name=result['name'],
            description=result['description'],
            category_id=result['category'])
        db.session.add(new_exercise)

    rest = Exercise(
        id=500,
        name='Rest',
        description='Take a breath, take a sip, get ready for the next round!',
        category_id=1)
    db.session.add(rest)

    db.session.commit()

    return "Exercises Table Filled"


def fill_images():
    """Fill equipment_images table with external API data"""
    response = requests.get(
        f"{API_BASE_URL}exerciseimage/?limit=120", headers=headers)

    res_json = response.json()
    results = res_json['results']

    pattern = "images/(.*?)/"

    for result in results:
        image_url = result['image']
        exercise_id = re.search(pattern, image_url).group(1)
        exercise_id = int(exercise_id)
        if(Exercise.query.get(exercise_id)):
            new_img = ExerciseImage(
                id=result['id'],
                exercise_id=exercise_id,
                image_url=image_url)
            db.session.add(new_img)

    db.session.commit()

    return "Exercise Images Table Filled"


def fill_exercises_equipment():
    """Fill exercises_equipment table using external API data."""
    response = requests.get(
        f"{API_BASE_URL}/exercise/?language=2&limit=231", headers=headers)

    res_json = response.json()
    results = res_json['results']

    for result in results:
        if (result['equipment'] != []):
            for equipment_id in result['equipment']:
                new_exercise_equipment = ExerciseEquipment(
                    exercise_id=result['id'],
                    equipment_id=equipment_id)
                db.session.add(new_exercise_equipment)

    db.session.commit()

    return "Exercises Equipment Table Filled"


def create_sample_user():
    sample_user = User.register(username='Test1', password="Password5")
    db.session.add(sample_user)
    db.session.commit()


def create_sample_workout():
    sample_user = User.query.filter_by(username='Test1').one()
    sample_workout = Workout(
        user_id=sample_user.id,
        type="AMRAP",
        name="Sample Bodyweight AMRAP",
        stages=3,
        stage_time=5
    )
    db.session.add(sample_workout)
    db.session.commit()


def build_sample_workout():
    ex1 = WorkoutExercise(
        workout_id=1,
        order=1,
        exercise_id=195,
        count=10,
        count_type="reps")
    ex2 = WorkoutExercise(
        workout_id=1,
        order=2,
        exercise_id=326,
        count=10,
        count_type="reps")
    ex3 = WorkoutExercise(
        workout_id=1,
        order=3,
        exercise_id=874,
        count=20,
        count_type="reps")
    ex4 = WorkoutExercise(
        workout_id=1,
        order=4,
        exercise_id=500,
        count=60,
        count_type="seconds")
    ex5 = WorkoutExercise(
        workout_id=1,
        order=5,
        exercise_id=238,
        count=10,
        count_type="reps")
    ex6 = WorkoutExercise(
        workout_id=1,
        order=6,
        exercise_id=338,
        count=10,
        count_type="seconds")
    ex7 = WorkoutExercise(
        workout_id=1,
        order=7,
        exercise_id=795,
        count=10,
        count_type="reps")
    ex8 = WorkoutExercise(
        workout_id=1,
        order=8,
        exercise_id=500,
        count=60,
        count_type="seconds")
    ex9 = WorkoutExercise(
        workout_id=1,
        order=9,
        exercise_id=879,
        count=20,
        count_type="reps")
    ex10 = WorkoutExercise(
        workout_id=1,
        order=10,
        exercise_id=330,
        count=10,
        count_type="reps")
    ex11 = WorkoutExercise(
        workout_id=1,
        order=11,
        exercise_id=387,
        count=30,
        count_type="seconds")

    db.session.add_all([
        ex1,
        ex2,
        ex3,
        ex4,
        ex5,
        ex6,
        ex7,
        ex8,
        ex9,
        ex10,
        ex11])
    db.session.commit()


def execute_all():
    db.drop_all()
    db.create_all()
    fill_categories()
    fill_equipment()
    fill_exercises()
    fill_images()
    fill_exercises_equipment()
    create_sample_user()
    create_sample_workout()
    build_sample_workout()

execute_all()
