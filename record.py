import datetime
from pytz import timezone

from uberAPI import requestUberData
from database_schema import Locations, RideData, UberXData, session, DayTimeIntervals, UberXMean
from utils import averageData, getTimeZoneOffset, roundTime, defineUTC

from sqlalchemy import exists

def addLocation(newLat, newLong, newName, locTimezone):
    new_location = Locations(latitude=newLat, longitude=newLong, name=newName, timezone=locTimezone)
    session.add(new_location)
    session.commit()

def addFareEstimate(start, end, timezone, newSurge, newHigh, newLow, newMin, newDistance, newDuration, newService):
    utc_time = defineUTC(datetime.datetime.utcnow())
    timeZoneDelta = getTimeZoneOffset(timezone)
    new_fare_estimate = RideData(start_location_id=start, end_location_id=end, surge=newSurge, \
        highEstimate=newHigh, lowEstimate=newLow, minimum=newMin, distance=newDistance, \
        service=newService, duration=newDuration, timestamp = utc_time , \
        timestamp_interval=defineUTC(roundTime(datetime.datetime.utcnow())), \
        timestamp_interval_EST=roundTime(datetime.datetime.utcnow())-timeZoneDelta)
    session.add(new_fare_estimate)
    session.commit()

######### Remove Block #########
def addUberX(start, end, timezone, newSurge, newHigh, newLow, newMin, newDistance, newDuration):
    utc_time = defineUTC(datetime.datetime.utcnow())
    timeZoneDelta = getTimeZoneOffset(timezone)
    new_fare_estimate = UberXData(start_location_id=start, end_location_id=end, surge=newSurge, \
        highEstimate=newHigh, lowEstimate=newLow, minimum=newMin, distance=newDistance, \
        duration=newDuration, timestamp = utc_time , \
        timestamp_interval=defineUTC(roundTime(datetime.datetime.utcnow())), \
        timestamp_interval_EST=roundTime(datetime.datetime.utcnow())-timeZoneDelta)
    session.add(new_fare_estimate)
    session.commit()
######### Remove Block #########

def addUberPOOLFareEstimate(start, end, timezone, newSurge, newHigh, newLow, newEstimate, newDistance, newDuration, newService):
    utc_time = defineUTC(datetime.datetime.utcnow())
    timeZoneDelta = getTimeZoneOffset(timezone)
    new_fare_estimate = RideData(start_location_id=start, end_location_id=end, surge=newSurge, \
        highEstimate=newHigh, lowEstimate=newLow, estimate=newEstimate, distance=newDistance, \
        service=newService, duration=newDuration, timestamp = utc_time , \
        timestamp_interval=defineUTC(roundTime(datetime.datetime.utcnow())), \
        timestamp_interval_EST=roundTime(datetime.datetime.utcnow())-timeZoneDelta)
    session.add(new_fare_estimate)
    session.commit()

def pullRecordUber(startLoc, endLoc):
    uberServices = ['POOL',
    'uberX', 
    'uberXL', 
    'UberSELECT', 
    'UberBLACK',
    'UberSUV']

    start_location = session.query(Locations).filter(Locations.name == startLoc).one()
    end_location = session.query(Locations).filter(Locations.name == endLoc).one()

    for items in uberServices:
        currentData = requestUberData(items, start_location.latitude, start_location.longitude, \
            end_location.latitude, end_location.longitude)
######### Remove Block #########
        #if items == 'uberX':
            #addUberX(start_location.id, end_location.id, start_location.timezone, currentData['surge'], \
                #currentData['highEstimate'], currentData['lowEstimate'], currentData['minimum'], \
                #currentData['distance'], currentData['duration'])
######### Remove Block #########
        if checkForFareChange(start_location.id, end_location.id, items, currentData):
            if currentData['minimum'] == None:
                addUberPOOLFareEstimate(start_location.id, end_location.id, start_location.timezone, currentData['surge'], \
                    currentData['highEstimate'], currentData['lowEstimate'], currentData['estimate'], \
                    currentData['distance'], currentData['duration'], items)
            elif currentData['estimate'] == None:
                addFareEstimate(start_location.id, end_location.id, start_location.timezone, currentData['surge'], \
                    currentData['highEstimate'], currentData['lowEstimate'], currentData['minimum'], \
                    currentData['distance'], currentData['duration'], items)

def pullUberX(startLoc, endLoc):
    start_location = session.query(Locations).filter(Locations.name == startLoc).one()
    end_location = session.query(Locations).filter(Locations.name == endLoc).one()

    currentData = requestUberData("uberX", start_location.latitude, start_location.longitude, \
        end_location.latitude, end_location.longitude)

    addUberX(start_location.id, end_location.id, start_location.timezone, currentData['surge'], \
        currentData['highEstimate'], currentData['lowEstimate'], currentData['minimum'], \
        currentData['distance'], currentData['duration'])

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

def updateUberXData(startLoc, endLoc):
    start_location = session.query(Locations).filter(Locations.name == startLoc).one()
    end_location = session.query(Locations).filter(Locations.name == endLoc).one()

    uberXEntry = requestUberData('uberX', start_location.latitude, start_location.longitude, \
        end_location.latitude, end_location.longitude)

    timeZoneDelta = getTimeZoneOffset(start_location.timezone)
    time_interval = roundTime(datetime.datetime.utcnow())-timeZoneDelta
    weekday_index = time_interval.weekday()
    time = time_interval.time()

    dayTimeInterval_record = session.query(DayTimeIntervals).filter(DayTimeIntervals.day_index==weekday_index). \
        filter(DayTimeIntervals.time_interval==time).first()

    print dayTimeInterval_record.id
    updateUberXMean(start_location.id, end_location.id, dayTimeInterval_record.id, uberXEntry)

def updateUberXMean(start_loc_id, end_loc_id, dayTimeInterval_id, uberXEntry):
    uberXMean_record = session.query(UberXMean).filter(UberXMean.day_time_interval_id==dayTimeInterval_id). \
        filter(UberXMean.start_location_id==start_loc_id). \
        filter(UberXMean.end_location_id==end_loc_id).first()

    if uberXMean_record == None:
        # No current Mean records exists for that timestamp and route
        new_uberX_mean = UberXMean(start_location_id=start_loc_id, end_location_id=end_loc_id, \
        surge=uberXEntry['surge'], highEstimate=uberXEntry['highEstimate'], lowEstimate=uberXEntry['lowEstimate'], \
        minimum=uberXEntry['minimum'], distance=uberXEntry['distance'], duration=uberXEntry['duration'],  \
        day_time_interval_id= dayTimeInterval_id, data_points=1 )
        session.add(new_uberX_mean)
        session.commit()
        print 'Added New Record'
    else:
        # Update Surge
        print uberXMean_record.surge, uberXMean_record.data_points
        uberXMean_record.surge = averageData(uberXMean_record.surge, uberXMean_record.data_points, uberXEntry['surge'])
        session.commit()
        print uberXMean_record.surge
        # Update highEstimate
        uberXMean_record.highEstimate = averageData(uberXMean_record.highEstimate, uberXMean_record.data_points, uberXEntry['highEstimate'])
        session.commit()
        # Update lowEstimate
        uberXMean_record.lowEstimate = averageData(uberXMean_record.lowEstimate, uberXMean_record.data_points, uberXEntry['lowEstimate'])
        session.commit()
        # Update Minimum
        uberXMean_record.minimum = averageData(uberXMean_record.minimum, uberXMean_record.data_points, uberXEntry['minimum'])
        session.commit()
        # Update Distance
        uberXMean_record.distance = averageData(uberXMean_record.distance, uberXMean_record.data_points, uberXEntry['distance'])
        session.commit()
        # Update Duration
        uberXMean_record.duration = averageData(uberXMean_record.duration, uberXMean_record.data_points, uberXEntry['duration'])
        session.commit()
        # Update Data Points
        uberXMean_record.data_points = uberXMean_record.data_points + 1
        session.commit()
        print uberXMean_record.data_points
        print 'Updated Record'


# Execute
#updateUberXData('jb3', 'Buckhead')