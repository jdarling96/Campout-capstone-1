from distutils.command.config import config
from fileinput import filename
import os
import re
import pandas as pd
from sqlalchemy import false
from app import db, app
from models import States

postgres = os.environ.get('DATABASE_URL')

db.drop_all()

db.create_all()

file_name = 'generator/states.csv'
load = pd.read_csv(file_name)

load.to_sql(name='states', con='postgresql://gmbwlnckliwcsi:49bae01d9cdb3cf4b330d3a9693a768e43ae9256ddf2503401aa1208ea26272c@ec2-23-23-151-191.compute-1.amazonaws.com:5432/dedg0dca48069t', if_exists='append', index=false)