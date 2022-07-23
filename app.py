from crypt import methods
import email
import os
import requests
import xmltodict
import pprint
import xml.etree.cElementTree as et
from flask import Flask, render_template, request, flash, redirect, session, g
from models import db, connect_db, User, CampgroundData, Campground, Favorites, SavedSite, States
from forms import UserAddForm, UserLoginForm, SearchCampground
from sqlalchemy.exc import IntegrityError

from flask_debugtoolbar import DebugToolbarExtension
from bs4 import BeautifulSoup

app = Flask(__name__)

app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///campout'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False 
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "campout")

toolbar = DebugToolbarExtension(app)


connect_db(app)
API_URL = 'http://api.amp.active.com/camping/campgrounds/?'
TOKEN = 'crkt92prkygkp3h6j7kb62c2'
FACILTYPHOTO_BASE_URL = 'http://www.reserveamerica.com'
CURR_USER_KEY = "curr_user"


@app.before_request
def add_user_to_g():
    """if user.id in session add curr user to Flask global"""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
        

    else:
        g.user = None
        


def do_login(user):
    """Log in user."""
    
    session[CURR_USER_KEY] = user.id
   


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]



@app.route('/')
def check_info():
    """Homepage for Campout"""
    return render_template('home.html')


@app.route('/about')
def display_about_page():
    """About page for Campout"""
    return render_template('about.html')


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    """Create new user and add to DB. Redirect to home page.
    If form not valid, present form.
    If the there already is a user with that username: flash message
    and re-present form.
    """
    form = UserAddForm()
    form.state_id.choices = [(state.short_name, state.long_name)for state in States.query.all()]
    
    

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                state_id=form.state_id.data,
                city=form.city.data,
                site_type=form.site_type.data,
                )
            
            db.session.commit()
           
        
        except IntegrityError:
            flash('Username already in use', 'danger')
            return render_template('users/register.html', form=form)

        
        do_login(user)
        
        flash(f'Welcome {user.username}', 'success')
        return redirect('/')    

       

    else:
        return render_template('users/register.html', form=form)    



@app.route('/login', methods=['GET', 'POST'])
def login():
    """authenticat user and login.
    If form not valid, present form.
    if authentication is TRUE do_login()
    Redirect to Homepage.
    """    

    form = UserLoginForm()

    if form.validate_on_submit():
        user = User.auth(
            username=form.username.data,
            password=form.password.data
            )
        
        if user:
            do_login(user)
            flash(f'Welcome back, {user.username}!','success')
            return redirect('/')
            
        
        flash('Invalid credentials.', 'danger')

    return render_template('users/login.html', form=form)    



@app.route('/search', methods=['GET', 'POST'])
def search_campgrounds_form():

    """   if not g.user:
        flash('Please register/login first', 'danger')
        return redirect('login') """
    
    form = SearchCampground()
    form.state_id.choices = [(state.short_name, state.long_name)for state in States.query.all()]
    

    if form.validate_on_submit():
        
        form_data = [form.state_id.data,form.pname.data,form.site_type.data,form.amenity.data,form.eqplen.data,form.max_people.data,form.hookup.data,
        form.sewer.data,form.water.data,form.pull.data,form.pets.data,form.waterfront.data]
        wow = [data for data in form_data if data not in ['',0,None]]
        print(wow)
        return redirect('/')
        
        wow = [[data]for data in form_data if 0 not in data or '' not in data]
        """   print(form_data)
        return redirect('/') """

    
    return render_template('search.html', form=form)


