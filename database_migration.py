import database_schema_v1
import database_schema_v2


def transferLocations(sessions):
    location_records = sessions[0].query(database_schema_v1.Locations).all()
    for record in location_records:
        sessions[1].add(database_schema_v2.Locations(latitude=record.latitude, longitude=record.longitude, \
            name=record.name))
        sessions[1].commit()

def transferRideData(sessions):
    rideData_records = sessions[0].query(database_schema_v1.RideData).all()
    for record in rideData_records:
        sessions[1].add(database_schema_v2.RideData(start_location_id=record.start_location_id, \
            end_location_id=record.end_location_id, surge=record.surge, highEstimate=record.highEstimate, \
            lowEstimate=record.lowEstimate, minimum=record.minimum, distance=record.distance, \
            estimate=record.estimate, service=record.service, timestamp = record.datetime))
        sessions[1].commit()
