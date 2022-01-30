from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length

class UserAddForm(FlaskForm):
    """Form for Creating an Account"""
    
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    
class LoginForm(FlaskForm):
    """Login Form"""
    
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    
class SearchExerciseForm(FlaskForm):
    """Form for filtering exercises"""
    
    name = StringField('Filter by name:')
    category = SelectField('Filter by category:', choices=['<none>', 'Abs', 'Arms', 'Back', 'Calves', 'Chest', 'Legs', 'Shoulders'])
    equipment = SelectMultipleField('Available Equipment', choices=[('1', 'Barbell'), ('8', 'Bench'), ('3', 'Dumbell'), ('9', 'Incline bench'), ('10', 'Kettlebell'), ('6', 'Pull-up bar'), ('5', 'Swiss Ball'), ('2', 'SZ-Bar')])