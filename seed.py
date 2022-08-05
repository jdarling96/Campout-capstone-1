from distutils.command.config import config
from fileinput import filename
import pandas as pd
from sqlalchemy import false
from app import db, app
from models import States
 
db.drop_all()

db.create_all()

file_name = 'generator/states.csv'
load = pd.read_csv(file_name)

load.to_sql(name='states', con='postgresql://rwdeulyaxmrcda:167b888b467e918996cbf3f72e237315557ccba63783988fb02e859995bc1446@ec2-107-22-122-106.compute-1.amazonaws.com:5432/dfcvpit93qj6vh', if_exists='append', index=false)