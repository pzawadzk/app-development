from sqlalchemy import create_engine
from sqlalchemy import desc
from sqlalchemy.orm import sessionmaker
 
from puppies import Base, Shelter, Puppy
#from flask.ext.sqlalchemy import SQLAlchemy
from random import randint
import datetime
import random

since = datetime.datetime.now() - datetime.timedelta(days=9*30)

engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession()


#all_puppies = session.query(Puppy).filter(Puppy.dateOfBirth < since).order_by(desc('dateOfBirth')).all()

all_puppies = session.query(Puppy).join(Puppy.shelter).order_by(Shelter.name)

for  puppy in all_puppies:
	print puppy.name, puppy.dateOfBirth, puppy.weight, puppy.shelter.name


