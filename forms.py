from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, Length
from wtforms.widgets import TextArea




states = [(0, 'AK'), (1, 'AL'), (1, 'AL'),(2, 'AR'),(3, 'AZ'),(3, 'AZ'),(4, 'CA'),(5, 'CO'),(6, 'CT'), (7, 'DC'), (8, 'DE'),(9, 'FL'),(10, 'GA'),(11, 'HI'),(12, 'IA'),(13, 'ID'),(14, 'IL'), (15, 'IN'),(16, 'KS'),
(17, 'KY'),(18, 'LA'),(19, 'MA'),(20, 'MD'),(21, 'ME'),(22, 'MI'),(23, 'MN'),(24, 'MO'),(25, 'MS'),(26, 'MT'),(27, 'NC'),(28, 'ND'),(29, 'NE'),(30, 'NH'),(31, 'NJ'),(32, 'NM'),(33, 'NV'),(34, 'NY'),(35, 'OH'),
(36, 'OK'),(37, 'OR'),(38, 'PA'),(39, 'PR'),(40, 'RI'),(41, 'SC'),(42, 'SD'),(43, 'TN'),(44, 'TX'),(45, 'UT'),(46, 'VA'),(47, 'VT'),(48, 'WA'),(49, 'WI'),(50, 'WV'),(51, 'WY')]


class UserAddForm(FlaskForm):
    """Form for adding users to db"""

    username = StringField('Username', validators=[DataRequired(), 
    Length(min=8,max=15,message='Username must be a minimum of %(min)d and a maximum of %(max)d')])
    
    email = StringField('E-mail', validators=[DataRequired(), Email(message='Not a valid E-mail address')])
    
    password = PasswordField('Password', validators=[DataRequired(), 
    Length(min=6, max=18, message='Password must be a minimum of %(min)d and a maximum of %(max)d')])

    state_id = SelectField('State', choices=states)

    city = StringField('City', validators=[DataRequired()])

    site_type = SelectField('Camping Style', choices=[(2001,'RV'),(10001,'Cabins/Lodgings'),(2003,'Tent'),(2002, 'Trailer'),(9002,'Big Groups'),(9001,'Day Use'),(3001,'Horse Site'),(2004,'Boat Site')])




