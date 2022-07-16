from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, Length
from wtforms.widgets import TextArea
from models import States

states = States.get_states()

state_choices = []
for index, state in enumerate(states, start=1):
    state_choices.append((index, state))


class UserAddForm(FlaskForm):
    """Form for adding users to db"""

    username = StringField('Username', validators=[DataRequired(), 
    Length(min=8,max=15,message='Username must be a minimum of %(min)d and a maximum of %(max)d')])
    
    email = StringField('E-mail', validators=[DataRequired(), Email(message='Not a valid E-mail address')])
    
    password = PasswordField('Password', validators=[DataRequired(), 
    Length(min=6, max=18, message='Password must be a minimum of %(min)d and a maximum of %(max)d')])

    state_id = SelectField('State', choices=state_choices)

    city = StringField('City,', validators=[DataRequired()])

    site_type = SelectField('Camping Style', choices=[(2001,'RV'),(10001,'Cabins/Lodgings'),(2003,'Tent'),(2002, 'Trailer')(9002,'Big Groups')(9001,'Day Use'),(3001,'Horse Site'),(2004,'Boat Site')])

    


