from fileinput import filename
import pandas as pd
from sqlalchemy import false
from app import db
from models import States

db.drop_all()

db.create_all()

file_name = 'generator/states.csv'
load = pd.read_csv(file_name)

load.to_sql(name='states', con='postgresql:///campout', if_exists='append', index=false)