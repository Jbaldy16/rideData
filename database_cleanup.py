
import datetime

import database_schema_v2

def updateDateTime(session):
	rideData_records = session.query(database_schema_v2.RideData).all()
	for record in rideData_records:
		record.timestamp += datetime.timedelta(hours=4)
		session.commit()

def addRoundedTime(session):
	rideData_records = session.query(database_schema_v2.RideData).all()
	for record in rideData_records:
		record.timestamp_interval = roundTime(record.timestamp)
		session.commit()

def roundTime(dt=None, roundTo=300):
	if dt == None : dt = datetime.datetime.now()
	seconds = (dt - dt.min).seconds
	# // is a floor division, not a comment on following line:
	rounding = (seconds+roundTo/2) // roundTo * roundTo
	return dt + datetime.timedelta(0,rounding-seconds,-dt.microsecond)
