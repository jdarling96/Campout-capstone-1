"""SQLAlchemy models for Campout"""


from typing_extensions import Self
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy



bcrypt = Bcrypt()
db = SQLAlchemy()

class States(db.Model):
    """All US states for location parameter in API call"""

    __tablename__ = 'states'

    short_name = db.Column(
        db.Text,
        primary_key=True,
        unique=True
    )
    
    long_name = db.Column(
        db.Text,
        unique=True
    )



class User(db.Model):
    """User model for campout"""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )

    password = db.Column(
        db.Text,
        nullable=False
    )
    
    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    state_id = db.Column(
        db.Text,
        db.ForeignKey('states.short_name', ondelete='CASCADE')
    )

    city = db.Column(
        db.Text,
        nullable=False,
    )

    site_type = db.Column(
        db.Integer,
        nullable=True 
    )

    
    
    favorites = db.relationship(
        'Favorites',
        backref='users'
    )

    saved_site = db.relationship(
        'SavedSite',
        backref='users'
    )

        
    
    def __repr__(self) -> str:
        return f"<User #{self.id}: {self.username}, {self.email}, {self.state_id}"

    @classmethod
    def signup(cls, username, password, email, state_id, city, site_type):
        """Sign up user.
        
        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd,
            email=email,
            state_id=state_id,
            city=city,
            site_type=site_type
        )

        db.session.add(user)
        return user

    @classmethod
    def auth(cls, username, password):
        """ Find user based on auth arguments
        if users exists and password == hashed password
        return user object
        else return false """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        
        return False


class CampgroundData(db.Model):
    """Specific amenities for a favorited/saved campground """

    __tablename__ = 'campground_data'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

   
    pets = db.Column(
        db.Text,
        nullable=True
    )

    water = db.Column(
        db.Text,
        nullable=True
    )                  
    
    sewer = db.Column(
        db.Text,
        nullable=True
    )

    amps = db.Column(
        db.Text,
        nullable=True
    )
    
    eq_length = db.Column(
        db.Text,
        nullable=True
    )


    waterfront = db.Column(
       db.Text,
       nullable=True
    )

    landmark_lat = db.Column(
        db.Text,
        nullable=True
    )

    landmark_long = db.Column(
        db.Text,
        nullable=True
    )

    
    def __repr__(self) -> str:
        return f"<User #{self.id}, {self.landmark_lat}, {self.landmark_long}"


class Campground(db.Model):
    """Basic campground info for favorited/saved campgrounds"""

    __tablename__ = 'campground'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    camp_data_id = db.Column(
        db.Integer,
        db.ForeignKey('campground_data.id', ondelete='CASCADE')
    )

    facility_name = db.Column(
        db.Text,
        nullable=False
    )

    facility_photo = db.Column(
        db.Text,
        default='/static/images/defauly-pic.png'
    )

    state = db.Column(
        db.Text,
        nullable=False
    )

    facility_type = db.Column(
         db.Text,
         nullable=True
    )

    amenities = db.relationship(
        'CampgroundData',
        backref='campground'
    )

class Favorites(db.Model):
    """A users favorite campgrounds"""

    __tablename__ = 'favorites'

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade'),
        primary_key=True
    )

    camp_id = db.Column(
        db.Integer,
        db.ForeignKey('campground.id', ondelete='cascade'),
        primary_key=True

    )

    

class SavedSite(db.Model):
    """A users saved campgrounds for later"""

    __tablename__ = 'saved_site'

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade'),
        primary_key=True
    )

    camp_id = db.Column(
        db.Integer,
        db.ForeignKey('campground.id', ondelete='cascade'),
        primary_key=True

    )



""" camp_list = db.session.query(User, Favorites, Campground). \
    select_from(User).join(Favorites).join(Campground).all()"""


def connect_db(app):
    """Connect this database to provided Flask app."""

    db.app = app
    db.init_app(app)