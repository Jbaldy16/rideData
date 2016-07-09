import sqlite3
import sys

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DATETIME, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class Locations(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    name = Column(String, nullable=False)


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
    service = Column(String, nullable=False)
    datetime = Column(DATETIME, nullable=False)

engine = create_engine('sqlite:///RIDEDATA.db')

Base.metadata.create_all(engine)