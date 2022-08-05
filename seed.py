from distutils.command.config import config
from fileinput import filename
import os
import pandas as pd
from sqlalchemy import false
from app import db, app
from models import States

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///campout'))
db.drop_all()

db.create_all()

file_name = 'generator/states.csv'
load = pd.read_csv(file_name)

load.to_sql(name='states', con='DATABASE_URL', if_exists='append', index=false)