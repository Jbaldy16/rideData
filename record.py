import settings

import datetime
from pytz import timezone

from uberAPI import requestUberData
from database_cleanup import roundTime, defineUTC
from database_schema_v2 import Locations, RideData

from sqlalchemy import create_engine, exists
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL

engine = create_engine(URL(**settings.AWS_DATABASE))
 
DBSession = sessionmaker(bind=engine)
session = DBSession()

def addLocation(newLat, newLong, newName, locTimezone):
    new_location = Locations(latitude=newLat, longitude=newLong, name=newName, timezone=locTimezone)
    session.add(new_location)
    session.commit()

def addFareEstimate(start, end, newSurge, newHigh, newLow, newMin, newDistance, newDuration, newService, startTimezone):
    utc_time = defineUTC(datetime.datetime.utcnow())
    new_fare_estimate = RideData(start_location_id=start, end_location_id=end, surge=newSurge, \
        highEstimate=newHigh, lowEstimate=newLow, minimum=newMin, distance=newDistance, \
        service=newService, duration=newDuration, timestamp = utc_time , \
        timestamp_interval=defineUTC(roundTime(datetime.datetime.utcnow())), \
        timestamp_interval_EST=roundTime(datetime.datetime.utcnow())+datetime.timedelta(hours=-4))
    session.add(new_fare_estimate)
    session.commit()

def addUberPOOLFareEstimate(start, end, newSurge, newHigh, newLow, newEstimate, newDistance, newDuration, newService, startTimezone):
    utc_time = defineUTC(datetime.datetime.utcnow())
    new_fare_estimate = RideData(start_location_id=start, end_location_id=end, surge=newSurge, \
        highEstimate=newHigh, lowEstimate=newLow, estimate=newEstimate, distance=newDistance, \
        service=newService, duration=newDuration, timestamp = utc_time , \
        timestamp_interval=defineUTC(roundTime(datetime.datetime.utcnow())), \
        timestamp_interval_EST=roundTime(datetime.datetime.utcnow())+datetime.timedelta(hours=-4))
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
        if checkForFareChange(start_location.id, end_location.id, items, currentData):
            if currentData['minimum'] == None:
                addUberPOOLFareEstimate(start_location.id, end_location.id, currentData['surge'], \
                    currentData['highEstimate'], currentData['lowEstimate'], currentData['estimate'], \
                    currentData['distance'], currentData['duration'], items, start_location.timezone)
            elif currentData['estimate'] == None:
                addFareEstimate(start_location.id, end_location.id, currentData['surge'], \
                    currentData['highEstimate'], currentData['lowEstimate'], currentData['minimum'], \
                    currentData['distance'], currentData['duration'], items, start_location.timezone)

def checkForFareChange(startLocID, endLocID, strService, currentFare):
    if checkForPreviousEntry(startLocID, endLocID, strService):
        lastFare = session.query(RideData).filter(RideData.service == strService) \
        .filter(RideData.start_location_id == startLocID).filter(RideData.end_location_id == endLocID) \
        .order_by(RideData.id.desc()).first()
        if strService == 'uberPOOL':
            if (lastFare.surge != currentFare['surge'] or lastFare.highEstimate != currentFare['highEstimate'] or \
                lastFare.lowEstimate != currentFare['lowEstimate'] or lastFare.estimate != currentFare['estimate']):
                    return True
            else:
                    return False
        else:
            if (lastFare.surge != currentFare['surge'] or lastFare.highEstimate != currentFare['highEstimate'] or \
                lastFare.lowEstimate != currentFare['lowEstimate'] or lastFare.minimum != currentFare['minimum']):
                    return True
            else:
                    return False
    else:
        return True

def checkForPreviousEntry(startLocID, endLocID, strService):
    check = session.query(exists().where(RideData.service == strService) \
        .where(RideData.start_location_id == startLocID) \
        .where(RideData.end_location_id == endLocID)).scalar()
    return check


