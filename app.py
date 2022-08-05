import os
import requests
import xmltodict
from flask import Flask, render_template, request, flash, redirect, session, g, jsonify
from models import db, connect_db, User, CampgroundData, Campground, SavedSite, States
from forms import UserAddForm, UserLoginForm, SearchCampground, UserEditForm
from sqlalchemy.exc import IntegrityError
import numpy as np


from flask_debugtoolbar import DebugToolbarExtension
from bs4 import BeautifulSoup

app = Flask(__name__)

app.debug = False
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///campout'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False 
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "campout")

toolbar = DebugToolbarExtension(app)


connect_db(app)
API_URL = 'http://api.amp.active.com/camping/campgrounds/?'
TOKEN = 'api_key=crkt92prkygkp3h6j7kb62c2'
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
    if g.user:
        flash('Allready logged in', 'danger')
        return redirect('/') 


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
    """authenticate user and login.
    If form not valid, present form.
    if authentication is TRUE do_login()
    Redirect to Homepage.
    """ 
    if g.user:
        flash('Allready logged in', 'danger')
        return redirect('/')    

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

@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()

    flash('You have been logged out', 'success')
    return redirect('/')

@app.route('/search', methods=['GET', 'POST'])
def search_campgrounds_form():
    """Return search form that contains up to 12 
    filters to search for campgrounds from Active Networks API. Displays filtered campground results"""
    
    if not g.user:
        flash('Please register/login first', 'danger')
        return redirect('login')  
    
    form = SearchCampground()
    form.pstate.choices = [(state.short_name, state.long_name)for state in States.query.all()]
    

    if form.validate_on_submit():
        
        form_data = [(form.pstate.name ,form.pstate.data), (form.pname.name, form.pname.data),(form.site_type.name, form.site_type.data),
        (form.amenity.name, form.amenity.data),(form.eqplen.name, form.eqplen.data),
        (form.Maxpeople.name, form.Maxpeople.data),(form.hookup.name, form.hookup.data),
        (form.sewer.name, form.sewer.data),(form.water.name, form.water.data),(form.pull.name, form.pull.data),
        (form.pets.name, form.pets.data),(form.waterfront.name, form.waterfront.data)]
        data = [(k,v) for (k,v) in form_data if v not in ['',0,None]]
        """ print(data)  """
        
        

        response = requests.get(
            API_URL+TOKEN,
            params=[(k,v) for (k,v) in data]
        )
        if response:
            dict_data = xmltodict.parse(response.content)
            result_set = dict_data['resultset']
            try:
                result = dict_data['resultset']['result'] 
                if len(result) < 24:
                    camps = np.array_split(result, 1)
                    print(len(camps))
                if len(result) >= 24:
                    camps = np.array_split(result, 2)
                    print(len(camps))
                if len(result) >= 50:
                    camps = np.array_split(result, 4)
                    print(len(camps))
                if len(result) >= 100:
                    camps = np.array_split(result, 6)
                    print(len(camps))
            except KeyError:
                flash('Invalid search. Make sure fields are valid', 'danger')
                return redirect('/search')



        else:
            print('failed')
            
        
        return render_template('campgrounds.html', result_set=result_set, camps=camps, user=g.user)      

    
    return render_template('search.html', form=form)


@app.route('/search/save/<facility_name>', methods=['POST'])
def user_save_site(facility_name):
    """Save campground to db and users saved sites"""
    
    if not g.user.id:
        flash('Please register/login first', 'danger')
        return redirect('login')

    
    camp_data = CampgroundData(pets=request.form["pets"], water=request.form["water"], sewer=request.form["sewer"],
    amps=request.form["amps"], waterfront=request.form["waterfront"], landmark_lat=request.form['landmark_lat'],
    landmark_long=request.form['landmark_long'])
    db.session.add(camp_data)
    db.session.flush()
    db.session.refresh(camp_data)
    
        
    campground = Campground(camp_data_id=camp_data.id,  facility_name=request.form["facility_name"],  facility_photo=request.form["facility_photo"],
    state=request.form["state"], facility_type=request.form["facility_type"])
    
  
    db.session.add(campground)
    try:
        db.session.flush()
    except IntegrityError:
        flash('Site has allready been saved', 'danger')
        return redirect(request.referrer)        
    db.session.refresh(campground)
    save_site =SavedSite(user_id=g.user.id,camp_id=campground.id)
    db.session.add(save_site)
    
    db.session.commit()
    
       
    flash('Site has been saved', 'success')
    return redirect(request.referrer)
    


@app.route('/user/account/<int:user_id>')
def user_account(user_id):
    """Users account for saved sites and a recommendation list based off of saved sites"""
    
    if not g.user:
        flash('Please register/login first', 'danger')
        return redirect('login')


    user = User.query.get_or_404(g.user.id)    
    campgrounds = Campground.query.filter(Campground.id.in_([n.camp_id for n in user.saved_site]))    
    
    return render_template('users/account.html', user=g.user, campgrounds=campgrounds)


@app.route('/user/account/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user_account(user_id):
    """Edits user account info if user authentication is True"""
    
    if not g.user:
        flash('Please register/login first', 'danger')
        return redirect('login')

    user = User.query.get_or_404(g.user.id)
    form = UserEditForm(obj=user)
    form.state_id.choices = [(state.short_name, state.long_name)for state in States.query.all()]

    if form.validate_on_submit():
        
        user = User.auth(user.username, form.password.data)
        
        if user:
            user.username = form.username.data
            user.email = form.email.data
            user.state_id = form.state_id.data
            user.city = form.city.data
            user.site_type = form.site_type.data
            
            db.session.commit()
            
            flash('Account updated!', 'success')
            return redirect(f'/user/account/{user.id}')
        
        flash('Incorrect password', 'danger') 
        return redirect(f'/user/account/{user.id}')   
        
    return render_template('/users/edit.html', form=form, user=user)




@app.route('/api/users/account/saved')
def users_saved_sites():
    """Returns a users saved sites in JSON if user is authenticated"""
    
    if not g.user:
        return jsonify([{"auth_required" : 'Please Login'}])

    
    user = User.query.get_or_404(g.user.id)
    
    campgrounds = Campground.query.filter(Campground.id.in_([n.camp_id for n in user.saved_site]))
    
    
    return jsonify([  { "facility_name" : c.facility_name, "facility_photo" : c.facility_photo , 
        "state" : c.state, "facility_type" : c.facility_type}  for c in campgrounds])
        
        

    
@app.route('/api/user/account/saved/<facility_name>/delete', methods=['POST'])
def delete_saved_site(facility_name):
    """Removes a site from a users saved sites if user is authenticated"""
    
    if not g.user:
        return jsonify([{"auth_required" : 'Please Login'}])

    campground = Campground.query.filter_by(facility_name=facility_name).first()
    
    campground_data = CampgroundData.query.get(campground.camp_data_id)
    
    saved_site = SavedSite.query.filter(SavedSite.camp_id == campground.id).first()
    
    
    db.session.delete(saved_site)
    db.session.delete(campground)
    db.session.delete(campground_data)
    db.session.commit()

    flash('Saved site removed', 'success')
    return redirect(f'/user/account/{g.user.id}')


@app.route('/api/user/account/recommend')
def recommend_sites():
    """Returns a list of recommended sites in JSON if user is authenticated.
    recommended sites are based off of users saved sites"""
    
    if not g.user:
        return jsonify([{"auth_required" : 'Please Login'}])
        
    user = User.query.get_or_404(g.user.id)
    user_campgrounds = user.campgrounds
    camp_data = [[data.facility_name, data.amenities] for data in user_campgrounds]
    
    if len(user.campgrounds) == 0:
        return jsonify([]) 
    
    response = requests.get(
            API_URL+TOKEN,
            params=[('landmarkName',camp_data[0][0]), ('landmarkLat',camp_data[0][1].landmark_lat), ('landmarkLong', camp_data[0][1].landmark_long)]
        )
    if response:
            dict_data = xmltodict.parse(response.content)
            
            try:
                result = dict_data['resultset']['result']
                wow = result[:5]
                
                
                
            except KeyError:
                flash('Invalid search. Make sure fields are valid', 'danger')
                return redirect('/search')

    else:
        print('failed')

    return jsonify([{'user_id':g.user.id},result[1:7]])                    
   
       

@app.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND page."""

    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    """404 NOT FOUND page."""

    return render_template('500.html'), 500



@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req


