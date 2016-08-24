import settings

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Time
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Locations(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    name = Column(String, nullable=False)
    timezone = Column(String, nullable=False)

class Routes(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True)
    start_location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)
    end_location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)
    name = Column(String, nullable=True)

class RideServices(Base):
    __tablename__ = "rideServices"

    id = Column(Integer, primary_key=True)
    serviceName = Column(String, nullable=True)

class RideData(Base):
    __tablename__ = "rideData"
 
    id = Column(Integer, primary_key=True)
    start_location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)
    end_location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)
    surge = Column(Float, nullable=False)
    highEstimate = Column(Float, nullable=False)
    lowEstimate = Column(Float, nullable=False)
    minimum = Column(Float, nullable=True)
    estimate = Column(Float, nullable=True)
    distance = Column(Float, nullable=False) 
    duration = Column(Float, nullable=True)
    riders = Column(Integer, nullable=True)
    service = Column(String, nullable=False)
    timestamp = Column(DateTime(True), nullable=False)
    timestamp_interval = Column(DateTime(True), nullable=False)
    timestamp_interval_EST = Column(DateTime, nullable=True)

class UberXData(Base):
    __tablename__ = "uberXData"
 
    id = Column(Integer, primary_key=True)
    start_location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)
    end_location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)
    surge = Column(Float, nullable=False)
    highEstimate = Column(Float, nullable=False)
    lowEstimate = Column(Float, nullable=False)
    minimum = Column(Float, nullable=True)
    distance = Column(Float, nullable=False) 
    duration = Column(Float, nullable=True)
    timestamp = Column(DateTime(True), nullable=False)
    timestamp_interval = Column(DateTime(True), nullable=False)
    timestamp_interval_EST = Column(DateTime, nullable=True)

class UberXMedian(Base):
    __tablename__ = "uberXMedian"
 
    id = Column(Integer, primary_key=True)
    start_location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)
    end_location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)
    surge = Column(Float, nullable=False)
    highEstimate = Column(Float, nullable=False)
    lowEstimate = Column(Float, nullable=False)
    minimum = Column(Float, nullable=True)
    distance = Column(Float, nullable=False) 
    duration = Column(Float, nullable=True)
    day_time_interval_id = Column(Integer, ForeignKey('dayTimeIntervals.id'), nullable=False)
    data_points = Column(Integer, nullable=False)


class DayTimeIntervals(Base):
    __tablename__ = 'dayTimeIntervals'

    id = Column(Integer, primary_key=True)
    day = Column(String, nullable=False)
    day_index = Column(Integer, nullable=False)
    time_interval = Column(Time(True), nullable=False)


def db_connect(DATABASE_NAME):
    return create_engine(DATABASE_NAME)

def db_create(engine):
    Base.metadata.create_all(engine)

def db_session(engine):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session

def create_db(DATABASE_NAME):
    if DATABASE_NAME == 'AWS_TEST_DATABASE':
        db_create(db_connect(URL(**settings.AWS_TEST_DATABASE)))
    elif DATABASE_NAME == 'AWS_DATABASE':
        db_create(db_connect(URL(**settings.AWS_DATABASE)))
    else:
        'Not a Valid Database'

# Set Session
if settings.CURRENT_DATABASE == 'TEST':
    engine = db_connect(URL(**settings.AWS_TEST_DATABASE))
    session = db_session(engine)
elif settings.CURRENT_DATABASE == 'LIVE':
    engine = db_connect(URL(**settings.AWS_DATABASE))
    session = db_session(engine)
else:
    'Not a Valid Database'

# Create DB
db_create(db_connect(URL(**settings.AWS_TEST_DATABASE)))
