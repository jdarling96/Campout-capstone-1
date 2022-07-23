from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, SelectField, RadioField
from wtforms.validators import DataRequired, Email, Length, Optional
from wtforms.widgets import TextArea




""" states = [(0, 'AK'), (1, 'AL'), (2, 'AR'), (3, 'AZ'), (4, 'CA'), (5, 'CO'), (6, 'CT'), (7, 'DC'), (8, 'DE'),(9, 'FL'),(10, 'GA'),(11, 'HI'),(12, 'IA'),(13, 'ID'),(14, 'IL'), (15, 'IN'),(16, 'KS'),
(17, 'KY'),(18, 'LA'),(19, 'MA'),(20, 'MD'),(21, 'ME'),(22, 'MI'),(23, 'MN'),(24, 'MO'),(25, 'MS'),(26, 'MT'),(27, 'NC'),(28, 'ND'),(29, 'NE'),(30, 'NH'),(31, 'NJ'),(32, 'NM'),(33, 'NV'),(34, 'NY'),(35, 'OH'),
(36, 'OK'),(37, 'OR'),(38, 'PA'),(39, 'PR'),(40, 'RI'),(41, 'SC'),(42, 'SD'),(43, 'TN'),(44, 'TX'),(45, 'UT'),(46, 'VA'),(47, 'VT'),(48, 'WA'),(49, 'WI'),(50, 'WV'),(51, 'WY')]
 """

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

    state_id = SelectField('State')

    pname = StringField('Park Name', validators=[Optional()])

    site_type = SelectField('Site Type', coerce=int, choices=[(2001,'RV'),(10001,'Cabins/Lodgings'),
     (2003,'Tent'),(2002, 'Trailer'),(9002,'Big Groups'),(9001,'Day Use'),
     (3001,'Horse Site'),(2004,'Boat Site')], validators=[Optional()])


    amenity = SelectField('Campground Feature', coerce=int, choices=[(4001,'Biking'),(4002,'Boating'),
    (4003,'Equipment Rental'),(4004, 'Fishing'),(4005,'Golf'),(4006,'Hiking'),
    (4007,'Horseback Riding'),(4008,'Hunting'),(4009, 'Recreational Activities'),
    (4010, 'Scenic Trails'),(4011,'Sports'),(4012,'Beach/Water Activities'),(4013,'Winter Activities')]) 
        
    
    eqplen = IntegerField('Equipment Length', 
    validators=[Length(min=5, max=50, message='Equipment Length must be a minimum of %(min)d and a maximum of %(max)d')])
     

    max_people = StringField('Number of campers',
    validators=[Length(min=1, max=8, message='Number of campers must be a minimum of %(min)d and a maximum of %(max)d')])
        
    
    hookup = SelectField('Electric Hookup', 
    choices=[(3002,'15 Amps or More'),(3003,' 20 Amps or More'),
    (3004,'30 Amps or More'),(3005, '50 Amps or More')])
   
    
    sewer = RadioField('Sewer Hookup', choices=[(3007,'Y')])

    
    water = RadioField('Water Hookup', choices=[(3006,'Y')])

    pull = RadioField('Pull Through Driveway', choices=[(3008,'Y')])    
    

    pets = RadioField('Pets Allowed', choices=[(3010,'Y')])

    waterfront = RadioField('Waterfront Sites', choices=[(3011,'Y')])

  



    


