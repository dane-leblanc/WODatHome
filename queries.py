from models import db, Equipment, Category, Exercise, ExerciseImage

def get_equip_list(equipment_id_input):
    """Form list of equipment ids for equipment available for user""" 
    #Automatically include "none" and "gym mat" in equipment list.
    equip_list = [Equipment.query.get(7),Equipment.query.get(4)]
    for id in equipment_id_input:
        equip_list.append(Equipment.query.get(int(id)))
    return equip_list

def get_exercises(equip_list, name_input, category_input):
    """Form list of exercises based on user filters"""
    # Filter by category (if user did not select a category, do not include a category on the exercise filter)
    if category_input != '<none>':
        cat = Category.query.filter_by(name=category_input).one()
        
        all_exercises = Exercise.query.filter(Exercise.name.ilike(f'%{name_input}%'), Exercise.category_id == cat.id).all()
            
    else: 
        all_exercises = Exercise.query.filter(Exercise.name.ilike(f'%{name_input}%')).all()
        
    exercises = []
        # Check the equipment needed for each exercise against the equipment the user marked as 'available'. Remove any exercises that require equipment beyond what's available. 
        # Also remove exercises with no equipment listed as these seem to either have other items of info missing or require very specific gym (machine) equipment.
    for exercise in all_exercises:
            if set(exercise.equipment).issubset(set(equip_list)) == True and exercise.equipment != []:
                exercises.append(exercise)
                
    return exercises

def get_exercise_image(id):
    """Get the image associated with the exercise id from our db."""
    e_img = ExerciseImage.query.filter(ExerciseImage.exercise_id == id).first()
    return e_img