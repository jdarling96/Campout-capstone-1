
# Campout



## Screenshots

![campout-home](https://user-images.githubusercontent.com/28359915/183329373-b918da50-08a1-4529-82f4-83e33f57e456.png)

![campout-search](https://user-images.githubusercontent.com/28359915/183329510-2e0cedc3-2d7e-4787-86f7-cc13bd5ad533.png)

![campout-account](https://user-images.githubusercontent.com/28359915/183329640-22228909-3e04-4a81-b762-1bb47c2dedc3.png)


## Table of Contents

  
  [About](#about)
  
  [API Information](#api-information)
  
  [Technologies used](#technologies-used)
  
  [Features](#features)
  
  [Authentication](#authentication)
  
  [Setup](#setup)
  
  [Site Flow](#site-flow)
  
  [Database Schema](#database-schema)
  
  [Wire Frame](#wire-frame)
  
  [Features for Later](#features-for-later)
  



## About
  Campout merges modern technology and the great outdoors. Whether you're an amateur adventurer that just moved to a new state or a veteran outdoorsman that is native to your land, Campout lets you find new experiences. Campout is a site that is designed to let users find new campsites in their area as well as recommend users camping spots based on what they like. Utilizing the Active Access Campground API, users are able to find spots within their state that have much larger search criteria for amenities and camping needs. Users will also be able to save campsites that are then added to a database. Users will have a account page that displays there saved sites and recommendations. User's accounts are secured and authentication is required for multiple routes in the site. 



## API Information
  Utilizing the [Active Access Campground API](https://developer.active.com/docs/read/Campground_APIs), users are able to find spots within their state that have much larger search criteria for amenities and camping needs. The Campground APIs, backed by Reserve America's database, provides access to campground data for 97% of the US and Canada's national and state/provincial parks. The Campground API returns data in the format of XML. Campout handles this XML data on the backend and uses a popular library xmltodict that makes working with XML feel like you are working with JSON. The Lat and Long of a site is included in this data and can make for possible intergration of google maps API to get directions. Campout has a recommendation feature that also uses this data to make another API call and return the closest campgrounds based on the Lat and Long of saved sites.

## Technologies used
 * HTML
 * CSS
 * Bootstrap
 * Python
 * Flask
 * SQLAlchemy
 * Javascript
 * Jquery
 * Axios
 * Postgres
 * xmltodict
 * numpy
 * WTForms 
 * Bcrypt
 
## Features
 * Up to 10 filters to apply to when searching for a campground.
 * Users can search for a park with a partial name.
 * Users can save multiple campsites to visit later and is stored in the user account page.
 * Recommendation system that recommends users 6 different campsites based off of the location and amenities of saved sites.
 * Users can save sites directly from there recommendation list.
 
## Authentication
  Users need to create an account in order to search, save, and get a list of recommend sites. Usernames are unique and upon registration, user ids are stored in the the session with an encrypted key value pair. The backend ensures that before each route is accessible the user must be found in a global flask varaible. This prevents outside sources from accessing your account. All sensitive data pertaining to the the application and the application database are setup in Flask enviorment variables. All user passwords are hashed/salted using Bcrypt before being stored.

## Setup
  Create a Python virtual environment:
* $ python3 -m venv venv

* $ source venv/bin/activate(venv)

* pip install -r requirements.txt

* set up the database:

* (venv) $ createdb warbler

* (venv) $ python seed.py

* Start the server:

* (venv) $ flask run
 
 
## Site Flow

![campout site-flow](https://user-images.githubusercontent.com/28359915/183321446-7621e9c2-7f12-4ecf-8e2a-960e130ffbac.png)

## Database Schema

![campout-uml](https://user-images.githubusercontent.com/28359915/183321422-c9b3e745-78f6-44d9-8e53-9640ead50608.png)

## Wire Frame

![campout-wireframe](https://user-images.githubusercontent.com/28359915/178855729-91cd11a0-de67-4792-a7db-9ca184eb4162.png)

## Features for Later
 * Incorporate Google Maps API that utilize the Lat and Long coordinates for a campsite.
 * Use HTML Geolocation to display sites closest to the them.
 * Add a feature that allows users to review a campsite.
