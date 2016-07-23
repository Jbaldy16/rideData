import settings

from sqlalchemy import create_engine, exists
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import sessionmaker
import database_schema_OLD
import database_schema

databases = ['sqlite:///RIDEDATA.db',
    URL(**settings.AWS_DATABASE)]

engines = []
sessions = []
for dbconninfo in databases:
    engine = create_engine(dbconninfo)
    engines.append(engine)
    sessions.append(sessionmaker(bind=engine)())

def transferLocations():
    location_records = sessions[0].query(database_schema_OLD.Locations).all()
    for record in location_records:
        sessions[1].add(database_schema.Locations(latitude=record.latitude, longitude=record.longitude, \
            name=record.name))
        sessions[1].commit()

def transferRideData():
    rideData_records = sessions[0].query(database_schema_OLD.RideData).all()
    for record in rideData_records:
        sessions[1].add(database_schema.RideData(start_location_id=record.start_location_id, \
            end_location_id=record.end_location_id, surge=record.surge, highEstimate=record.highEstimate, \
            lowEstimate=record.lowEstimate, minimum=record.minimum, distance=record.distance, \
            estimate=record.estimate, service=record.service, datetime = record.datetime))
        sessions[1].commit()

#######################################
#transferLocations()
transferRideData()
