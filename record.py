
import sqlite3
import sys
import datetime

from uberAPI import requestUberData

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_schema import Base, Locations, RideData

engine = create_engine('sqlite:///RIDEDATA.db')
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
session = DBSession()

def addLocation(newLat, newLong, newName):
    new_location = Locations(latitude=newLat, longitude=newLong, name=newName)
    session.add(new_location)
    session.commit()

def addFareEstimate(start, end, newSurge, newHigh, newLow, newMin, newDistance, newService):
    new_fare_estimate = RideData(start_location_id=start, end_location_id=end, surge=newSurge, \
        highEstimate=newHigh, lowEstimate=newLow, minimum=newMin, distance=newDistance, \
        service=newService, datetime = datetime.datetime.now())
    session.add(new_fare_estimate)
    session.commit()

def addUberPOOLFareEstimate(start, end, newSurge, newHigh, newLow, newEstimate, newDistance, newService):
    new_fare_estimate = RideData(start_location_id=start, end_location_id=end, surge=newSurge, \
        highEstimate=newHigh, lowEstimate=newLow, estimate=newEstimate, distance=newDistance, \
        service=newService, datetime = datetime.datetime.now())
    session.add(new_fare_estimate)
    session.commit()

def pullRecordUber(startLoc, endLoc):
    uberServices = ['uberPOOL', 
    'uberX', 
    'uberXL', 
    'uberSELECT', 
    'uberBLACK',
    'uberSUV']

    start_location = session.query(Locations).filter(Locations.name == startLoc).one()
    end_location = session.query(Locations).filter(Locations.name == endLoc).one()

    for items in uberServices:
        currentData = requestUberData(items, start_location.latitude, start_location.longitude, \
            end_location.latitude, end_location.longitude)
        if currentData['minimum'] == None:
            addUberPOOLFareEstimate(start_location.id, end_location.id, currentData['surge'], \
                currentData['highEstimate'], currentData['lowEstimate'], currentData['estimate'], \
                currentData['distance'], items)
        elif currentData['estimate'] == None:
            addFareEstimate(start_location.id, end_location.id, currentData['surge'], \
                currentData['highEstimate'], currentData['lowEstimate'], currentData['minimum'], \
                currentData['distance'], items)
