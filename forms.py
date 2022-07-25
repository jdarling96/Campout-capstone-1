from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, SelectField, RadioField, FloatField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange
from wtforms.widgets import TextArea



class UserAddForm(FlaskForm):
    """Form for adding users to db"""

    username = StringField('Username', validators=[DataRequired(), 
    Length(min=8,max=15,message='Username must be a minimum of %(min)d and a maximum of %(max)d')])
    
    email = StringField('E-mail', validators=[DataRequired(), Email(message='Not a valid E-mail address')])
    
    password = PasswordField('Password', validators=[DataRequired(), 
    Length(min=6, max=18, message='Password must be a minimum of %(min)d and a maximum of %(max)d')])

    state_id = SelectField('State')

    city = StringField('City', validators=[DataRequired()])

    site_type = SelectField('Camping Style',coerce=int, choices=[(2001,'RV'),(10001,'Cabins/Lodgings'),(2003,'Tent'),(2002, 'Trailer'),(9002,'Big Groups'),(9001,'Day Use'),(3001,'Horse Site'),(2004,'Boat Site')])


class UserLoginForm(FlaskForm):
    """Form for logging in registered users"""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])



class SearchCampground(FlaskForm):
    """Form for searching for campground based on API filters"""

    pstate = SelectField('State')

    pname = StringField('Park Name', validators=[Optional()])

    site_type = SelectField('Site Type', coerce=int, choices=[(0,''),(2001,'RV'),(10001,'Cabins/Lodgings'),
     (2003,'Tent'),(2002, 'Trailer'),(9002,'Big Groups'),(9001,'Day Use'),
     (3001,'Horse Site'),(2004,'Boat Site')])


    amenity = SelectField('Campground Feature', coerce=int, choices=[(0,''),(4001,'Biking'),(4002,'Boating'),
    (4003,'Equipment Rental'),(4004, 'Fishing'),(4005,'Golf'),(4006,'Hiking'),
    (4007,'Horseback Riding'),(4008,'Hunting'),(4009, 'Recreational Activities'),
    (4010, 'Scenic Trails'),(4011,'Sports'),(4012,'Beach/Water Activities'),(4013,'Winter Activities')]) 
        
    
    eqplen = IntegerField('Equipment Length', 
    validators=[NumberRange(min=5, max=50, message='Equipment Length must be a minimum of %(min)d and a maximum of %(max)d'),Optional()])
     

    Maxpeople = StringField('Number of campers',
    validators=[Length(min=1, max=8, message='Number of campers must be a minimum of %(min)d and a maximum of %(max)d'),Optional()])
        
    
    hookup = SelectField('Electric Hookup',
    choices=[('',''),('3002','15 Amps or More'),('3003',' 20 Amps or More'),
    ('3004','30 Amps or More'),('3005', '50 Amps or More')])
   
    
    sewer = SelectField('Sewer Hookup', choices=[('',''),('3007','Y')])

    
    water = SelectField('Water Hookup', choices=[('',''),('3006','Y')])

    pull = SelectField('Pull Through Driveway', choices=[('',''),('3008','Y')])    
    

    pets = SelectField('Pets Allowed', choices=[('',''),('3010','Y')])

    waterfront = SelectField('Waterfront Sites', choices=[('',''),('3011','Y')])

  



    


