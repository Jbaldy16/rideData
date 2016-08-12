import settings
import settings

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.engine.url import URL

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

def db_connect(DATABASE_NAME):
    return create_engine(DATABASE_NAME)

def db_create(engine):
    Base.metadata.create_all(engine)