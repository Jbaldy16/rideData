import datetime
from pytz import timezone

import database_schema
from database_cleanup import roundTime, defineUTC

def transferLocations(sessions):
    location_records = sessions[0].query(database_schema.Locations).all()
    for record in location_records:
        sessions[1].add(database_schema.Locations(latitude=record.latitude, longitude=record.longitude, \
            name=record.name, timezone='US/Eastern'))
        sessions[1].commit()

def transferRideData(sessions):
    rideData_records = sessions[0].query(database_schema.RideData).filter(database_schema.RideData.service=='uberX'). \
    filter(database_schema.RideData.start_location_id==1).filter(database_schema.RideData.end_location_id==3).all()
    for record in rideData_records:
        sessions[1].add(database_schema.RideData(start_location_id=record.start_location_id, \
            end_location_id=record.end_location_id, surge=record.surge, highEstimate=record.highEstimate, \
            lowEstimate=record.lowEstimate, minimum=record.minimum, distance=record.distance, \
            estimate=record.estimate, service=record.service,
            timestamp=record.timestamp, timestamp_interval=record.timestamp_interval, \
            timestamp_interval_EST=record.timestamp_interval_EST))
        sessions[1].commit()

def transferSample(sessions):
    rideData_records = sessions[0].query(database_schema.RideData).filter(database_schema.RideData.id<4073). \
        order_by(database_schema.RideData.id)
    for record in rideData_records:
        sessions[1].add(database_schema.RideData(start_location_id=record.start_location_id, \
            end_location_id=record.end_location_id, surge=record.surge, highEstimate=record.highEstimate, \
            lowEstimate=record.lowEstimate, minimum=record.minimum, distance=record.distance, \
            estimate=record.estimate, service=record.service,
            timestamp=record.timestamp, timestamp_interval=record.timestamp_interval, \
            timestamp_interval_EST=record.timestamp_interval_EST))
        sessions[1].commit()