import settings

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey

Base = declarative_base()

class Locations(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    name = Column(String, nullable=False)

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
    datetime = Column(DateTime, nullable=False)

def db_connect():
    return create_engine(URL(**settings.AWS_DATABASE))

def db_create(engine):
    Base.metadata.create_all(engine)
