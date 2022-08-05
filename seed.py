from distutils.command.config import config
from fileinput import filename
import os
import re
import pandas as pd
from sqlalchemy import false
from app import db, uri
from models import States



db.drop_all()

db.create_all()

file_name = 'generator/states.csv'
load = pd.read_csv(file_name)

load.to_sql(name='states', con=uri, if_exists='append', index=false)