from sqlalchemy import Column, DateTime, String, Integer, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
import ConfigParser
import os
import memcache
import json

Base = declarative_base()


class DTR(Base):
    __tablename__ = 'dtr'
    id = Column(Integer, primary_key=True)
    time_login = Column(DateTime, default=func.now())
    id_number = Column(String)
    synced = Column(Integer, default=0)
    kind = Column(String)


class Student(Base):
    __tablename__ = 'Student'
    id = Column(String, primary_key=True)
    id_number = Column(String)
    full_name = Column(String)
    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)
    section = Column(String)
    level = Column(String)
    rfid = Column(String)
    image = Column(String)
    id_picture = Column(String)
    school_year = Column(String)
    created_on = Column(DateTime, default=func.now())
    updated_on = Column(DateTime, default=func.now())
    kind = Column(String)
    chinese_name = Column(String)
    lunch_pass = Column(String)
    commuter_pass = Column(String)


Config = ConfigParser.ConfigParser()
Config.read("{0}/rfid.ini".format(os.path.dirname(os.path.abspath(__file__))))
url = Config.get('site', 'url', 0)
username = Config.get('site', 'username', 0)
password = Config.get('site', 'password', 0)
image_path = Config.get('data', 'image_path', 0)
db_path = Config.get('data', 'db_path', 0)
school_year = Config.get('data', 'school_year', 0)
school_name = Config.get('data', 'school_name', 0)
time_diff = Config.get('data', 'time_diff', 0)

if not os.path.exists(image_path):
    os.makedirs(image_path)
if not os.path.exists(db_path):
    os.makedirs(db_path)

kind = Config.get('data', 'kind', 0)
engine = create_engine('sqlite:///{0}/rfid.sqlite'.format(db_path), connect_args={'timeout': 15})
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)


def get_time():
    shared = memcache.Client(['127.0.0.1:11211'], debug=0)
    diff = time_diff
    if shared.get('connection'):
        message = json.loads(shared.get('connection'))
        try:
            diff = message['time_diff']
        except:
            diff = time_diff
    try:
        int_diff = int(diff)
    except:
        int_diff = 0

    return datetime.datetime.now() + datetime.timedelta(minutes=int_diff)

