from crypt import methods
import os
import requests
import xmltodict
import pprint
import xml.etree.cElementTree as et
from flask import Flask, render_template, request, flash, redirect, session, g
from models import db, connect_db, User, CampgroundData, Campground, Favorites, SavedSite, States
from forms import UserAddForm

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

token = 'crkt92prkygkp3h6j7kb62c2'
FACILTYPHOTO_BASE_URL = 'http://www.reserveamerica.com'
CURR_USER_KEY = "curr_user"
USER_TOKEN = 'curr_user_token'

@app.before_request
def add_user_to_g():
    """if user.id in session add curr user to Flask global"""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
        g.token = token

    else:
        g.user = None
        g.token = None


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

    return render_template('register.html', form=form)

    """  if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data
            )  """