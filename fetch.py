"""Use these functions to fill our database with data from wger API"""
import requests
import re
from models import db, Category, Exercise, Equipment, ExerciseImage, ExerciseEquipment

from secret import API_SECRET_KEY

API_BASE_URL = 'https://wger.de/api/v2/'

headers = {
    "Authorization": f"Token {API_SECRET_KEY}",
    "Accept": "application/json; indent=4"
    }

def fill_categories():
    """Fill categories table with external API data"""
        
    response = requests.get(f"{API_BASE_URL}exercisecategory", headers=headers)
    
    res_json = response.json()
    results = res_json['results']
    
    for result in results:
        new_category = Category(id=result['id'], name=result['name'])
        db.session.add(new_category)
        
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
    response = requests.get(f"{API_BASE_URL}/exercise/?language=2&limit=231", headers=headers)
    
    res_json = response.json()
    results = res_json['results']
    
    for result in results:
        new_exercise = Exercise(
            id=result['id'],
            name=result['name'],
            description=result['description'],
            category_id=result['category']
            )
        db.session.add(new_exercise)
    db.session.commit()
    
    return "Exercises Table Filled"

def fill_images():
    """Fill equipment_images table with external API data"""
    response = requests.get(f"{API_BASE_URL}exerciseimage/?limit=120", headers=headers)
    
    res_json = response.json()
    results = res_json['results']
    
    pattern = "images/(.*?)/"
    
    for result in results:
        image_url = result['image']
        exercise_id = re.search(pattern, image_url).group(1)
        exercise_id = int(exercise_id)
        if(Exercise.query.get(exercise_id)):
            new_img = ExerciseImage(id=result['id'],exercise_id=exercise_id, image_url=image_url)
            db.session.add(new_img)
        
    db.session.commit()
    
    return "Exercise Images Table Filled"

def fill_exercises_equipment():
    """Fill exercises_equipment table using external API data."""
    response = requests.get(f"{API_BASE_URL}/exercise/?language=2&limit=231", headers=headers)
    
    res_json = response.json()
    results = res_json['results']
    
    for result in results:
        if (result['equipment'] != []):
            for equipment_id in result['equipment']:
                new_exercise_equipment = ExerciseEquipment(
                    exercise_id=result['id'], 
                    equipment_id=equipment_id
                    )
                db.session.add(new_exercise_equipment)
                
    db.session.commit()
    
    return "Exercises Equipment Table Filled"