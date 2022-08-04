import json
import os
from this import d
from typing_extensions import Self
from unittest import TestCase
from webbrowser import get
from bs4 import BeautifulSoup
import pandas as pd
from requests import session
from sqlalchemy import exc, false
from models import *

os.environ['DATABASE_URL'] = "postgresql:///campout-test"

from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class UserViewTestCase(TestCase):
    """Test views for users"""

    def setUp(self):
        """Create test client, add sample data"""
        
        db.drop_all()
        db.create_all()
        
        file_name = 'generator/states.csv'
        load = pd.read_csv(file_name)

        load.to_sql(name='states', con='postgresql:///campout-test', if_exists='append', index=false)

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    password="testuser",
                                    email="test@test.com",
                                    state_id='CT',
                                    city='Lakewood',
                                    site_type=2003)
        self.testuser_id = 9000
        self.testuser.id = self.testuser_id

        camp_data = CampgroundData(pets='Y', water='N', sewer='N', amps='Y', waterfront='Lakefront', landmark_lat='39.3415944',
        landmark_long='-105.329625')

        db.session.add(camp_data)
        db.session.flush()
        db.session.refresh(camp_data)
    
        
        campground = Campground(camp_data_id=camp_data.id,  facility_name='BUFFALO CAMPGROUND',  facility_photo='http://www.reserveamerica.com/images/nophoto.jpg',
        state='CO', facility_type='FEDERAL')
        db.session.add(campground)
        db.session.flush()
        db.session.refresh(campground)
        save_site =SavedSite(user_id=self.testuser_id,camp_id=campground.id)
        db.session.add(save_site)

        db.session.commit()


    
    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp 

    def test_user_register_form(self):
        with self.client as c:
            resp = c.get('/register')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<form method="post" action="/register">', html)
            self.assertIn('<p class="h6 mb-2"><label for="username">Username</label></p>', html)
            self.assertIn('<p class="h6 mb-2"><label for="password">Password</label></p>', html)

    def test_user_register_success(self):
        with self.client as c:
            d = {'username':'testaccount1', 'password':'testpass', 'email':'testaccount@gmail.com','state_id':'CO',
            'city':'Littleton','site_type':2003}
            
            resp = c.post('/register', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)
            user = User.query.filter(User.username == d['username'])
            
            self.assertEqual(resp.status_code,200) 
            self.assertIn=('<div class="alert alert-success">Welcome testaccount1</div>', html)
            user = User.query.get(1)           
            db.session.delete(user)
             

    def test_user_register_fail(self):
        with self.client as c:
            d = {'username':'testuser', 'password':'testuser', 'email':'test@test.com','state_id':'CT',
            'city':'Lakewood','site_type':2003}
            resp = c.post('/register', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn=('<div class="alert alert-danger">Username already in use</div>', html)

    def test_user_login_form(self):
         with self.client as c:
            resp = c.get('/login')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<p class="h6 mb-2"><label for="username">Username</label></p>', html)
            self.assertIn('<p class="h6 mb-2"><label for="password">Password</label></p>', html)

    def test_user_login_success(self):
        with self.client as c:
            d = {'username':'testuser', 'password':'testuser'}
            resp = c.post('/login', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn=('<div class="alert alert-success">Welcome back, testuser</div>', html)

    def test_user_login_fail(self):
        with self.client as c:
            d = {'username':'testuser', 'password':'wrongpass'}
            resp = c.post('/login', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn=('<div class="alert alert-danger">Invalid credentials.</div>', html)

    def test_user_logout(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id
            
            resp = c.get('/logout')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertIn=('<div class="alert alert-success">You have been logged out</div>', html)
           
     
    def test_search_form(self):
          with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            resp = c.get('/search')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn=('<form method="post" action="/rsearch">', html)
    
    def test_search_form_unauthorized(self):
          with self.client as c:
            

            resp = c.get('/search')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertIn=('<div class="alert alert-danger">Please register/login first</div>', html)

    def test_search(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id
            
            d = {'pstate':'CO', 'pname':'buffalo', 'site_type': 2003}
            resp = c.post('/search', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn=('<p class="h6">Park: BUFFALO CAMPGROUND</p>', html)    
    
    
    
    
    def test_search_save_site(self):
          with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

             
                
            d = {'facility_photo':'http://www.reserveamerica.com/images/nophoto.jpg', 'facility_name':'BUFFALO CAMPGROUND', 'state':'CO',
            'facility_type':'FEDERAL', 'amps':'Y', 'pets':'Y', 'water':'N', 'sewer':'N', 
            'waterfront':'Lakefront','eq_length': '','landmark_lat':'39.3415944','landmark_long':'-105.329625'}
            
            fname = d['facility_name']
            resp = c.post('/search/save/BUFFALO CAMPGROUND', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertIn=('<div class="alert alert-success">Site has been saved</div>', html)  

                
    
    
    def test_user_account(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id
            
            resp = c.get('/user/account/9000')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn=("<h2 style=color: white;>testuser's Saved Sites</h2>", html)

   
    def test_user_account_unauthorized(self):
        with self.client as c:
            
                
            resp = c.get('/user/account/9000')
            html = resp.get_data(as_text=True)
                
            self.assertEqual(resp.status_code, 302)
            self.assertIn=('<div class="alert alert-danger">Please register/login first</div>', html)
                       
    
    
    def test_user_account_edit_form(self):
         with self.client as c:
             with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id
            
                
         resp = c.get('/user/account/9000/edit')
         html = resp.get_data(as_text=True)
                
         self.assertEqual(resp.status_code, 200)
         self.assertIn=('<form method="POST" id="user_form" action="/user/account/1/edit">', html)

    
    def test_user_account_edit(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            d = {'username':"testuser",'email':"test@test.com",'state_id':'CT','city':'Lakewood','site_type': 2003,'password': 'testuser'}
            resp = c.post('/user/account/9000/edit', data=d, follow_redirects=True) 

            html = resp.get_data(as_text=True)
                
            self.assertEqual(resp.status_code, 200)
            self.assertIn=('<div class="alert alert-success">Account updated!</div>', html)   
    
    
    def test_api_user_saved_sites_unauthorized(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = None

        resp = c.get('/api/users/account/saved')
        
                
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json[0], {"auth_required" : 'Please Login'})

    
    def test_api_user_saved_sites(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

        resp = c.get('/api/users/account/saved')
        
                
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json[0], {'facility_name': 'BUFFALO CAMPGROUND',
                                        'facility_photo': 'http://www.reserveamerica.com/images/nophoto.jpg',
                                        'facility_type': 'FEDERAL',
                                        'state': 'CO'})
    
     
    
    
    
    def test_api_user_recommend_sites(self):
         with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

         resp = c.get('/api/user/account/recommend')

         self.assertEqual(resp.status_code, 200)
         json_response = json.loads(resp.get_data(as_text=True))
         self.assertEqual(resp.json[1][0], 
                                           {'@agencyIcon': '', '@agencyName': '',
                                           '@contractID': 'FLST',
                                           '@contractType': 'FEDERAL',
                                           '@facilityID': '753545',
                                           '@facilityName': 'MEADOWS GROUP CAMPGROUND',
                                           '@faciltyPhoto': '/images/nophoto.jpg',
                                           '@favorite': 'N',
                                           '@latitude': '39.3319444',
                                           '@listingOnly': 'Y',
                                           '@longitude': '-105.3166667',
                                           '@regionName': '',
                                           '@shortName': 'USFS2545',
                                           '@sitesWithAmps': 'Y',
                                           '@sitesWithPetsAllowed': 'Y',
                                           '@sitesWithSewerHookup': 'N',
                                           '@sitesWithWaterHookup': 'N',
                                           '@sitesWithWaterfront': 'Lakefront',
                                           '@state': 'CO'})

    
    
    
    
    
    
    
    
    


