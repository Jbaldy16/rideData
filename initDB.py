import settings

import datetime
from pytz import timezone

from database_schema import session, DayTimeIntervals, UberXMean, UberXData, Locations, RideData
from utils import averageData, roundTime, defineUTC

def initDayTimeIntervalTable():
	Weekdays = ['Monday',
		'Tuesday',
		'Wednesday',
		'Thursday',
		'Friday',
		'Saturday',
		'Sunday']
	dayIndex = 0
	for weekday in Weekdays:
		j = 0
		while j<24:
			i = 0
			while i<60:
				time =  datetime.time(hour=j, minute=i)
				print time
				new_daytime = DayTimeIntervals(day=weekday, day_index=dayIndex, time_interval=time)
				session.add(new_daytime)
				session.commit()
				i = i + 5
			j = j + 1
		dayIndex = dayIndex + 1

def initUberXMeanTable(startLoc, endLoc):
	start_location = session.query(Locations).filter(Locations.name == startLoc).one()
	end_location = session.query(Locations).filter(Locations.name == endLoc).one()

	uberX_records = session.query(UberXData).filter(UberXData.start_location_id==start_location.id). \
		filter(UberXData.end_location_id==end_location.id)

	for uberXEntry in uberX_records:
		time_interval = uberXEntry.timestamp_interval_EST
		weekday_index = time_interval.weekday()
		time = time_interval.time()

		dayTimeInterval_record = session.query(DayTimeIntervals).filter(DayTimeIntervals.day_index==weekday_index). \
			filter(DayTimeIntervals.time_interval==time).first()

		uberXMean_record = session.query(UberXMean).filter(UberXMean.day_time_interval_id==dayTimeInterval_record.id). \
			filter(UberXMean.start_location_id==start_location.id). \
			filter(UberXMean.end_location_id==end_location.id).first()

		print uberXEntry.id

		if uberXMean_record == None:
			# No current Mean records exists for that timestamp and route
			new_uberX_mean = UberXMean(start_location_id=start_location.id, end_location_id=end_location.id, \
			surge=uberXEntry.surge, highEstimate=uberXEntry.highEstimate, lowEstimate=uberXEntry.lowEstimate, \
			minimum=uberXEntry.minimum, distance=uberXEntry.distance, duration=uberXEntry.duration,  \
			day_time_interval_id= dayTimeInterval_record.id, data_points=1 )
			session.add(new_uberX_mean)
			session.commit()
			print 'Added New Record'
		else:
			# Update Surge
			uberXMean_record.surge = averageData(uberXMean_record.surge, uberXMean_record.data_points, uberXEntry.surge)
			# Update highEstimate
			uberXMean_record.highEstimate = averageData(uberXMean_record.highEstimate, uberXMean_record.data_points, uberXEntry.highEstimate)
			# Update lowEstimate
			uberXMean_record.lowEstimate = averageData(uberXMean_record.lowEstimate, uberXMean_record.data_points, uberXEntry.lowEstimate)
			# Update Minimum
			uberXMean_record.minimum = averageData(uberXMean_record.minimum, uberXMean_record.data_points, uberXEntry.minimum)
			# Update Distance
			uberXMean_record.distance = averageData(uberXMean_record.distance, uberXMean_record.data_points, uberXEntry.distance)
			# Update Duration
			uberXMean_record.duration = averageData(uberXMean_record.duration, uberXMean_record.data_points, uberXEntry.duration)
			# Update Data Points
			uberXMean_record.data_points = uberXMean_record.data_points + 1
			session.commit()
			print 'Updated Record'

def interpolateUberXRecords(startLoc, endLoc):
	start_location = session.query(Locations).filter(Locations.name == startLoc).one()
	end_location = session.query(Locations).filter(Locations.name == endLoc).one()
	previous_record = session.query(RideData).filter(RideData.start_location_id==start_location.id). \
		filter(RideData.end_location_id==end_location.id). \
		filter(RideData.service=='uberX'). \
		order_by(RideData.timestamp_interval).first()
	rideData_records = session.query(RideData).filter(RideData.start_location_id==start_location.id). \
		filter(RideData.end_location_id==end_location.id). \
		filter(RideData.service=='uberX'). \
		order_by(RideData.timestamp_interval).all()
	for current_record in rideData_records:
		interval = datetime.timedelta(minutes=5)
		max_gap = datetime.timedelta(hours=20)
		gap = (current_record.timestamp_interval - previous_record.timestamp_interval)
		#print gap
		if gap <= interval:
			#print 'Added Record (1st Call): ', current_record.id
			addUberXRecord(current_record)
			previous_record = current_record
		elif gap > max_gap:
			print gap
			#print 'Added Record (2nd Call): ', current_record.id
			addUberXRecord(current_record)
			previous_record = current_record
		else:
			while gap > interval:
				#print 'Created New Record: ', previous_record.id, ' +5'
				addUberXRecord(previous_record, interval)
				interval = interval + datetime.timedelta(minutes=5)
			#print 'Added Record (3rd Call): ', current_record.id
			addUberXRecord(current_record)
			previous_record = current_record

def addUberXRecord(recordClass, interval=None):
	if interval==None:
		interval = datetime.timedelta(minutes=0)
	new_fare_estimate = UberXData(start_location_id=recordClass.start_location_id, end_location_id=recordClass.end_location_id, \
		surge=recordClass.surge, highEstimate=recordClass.highEstimate, lowEstimate=recordClass.lowEstimate, \
		minimum=recordClass.minimum, distance=recordClass.distance, duration=recordClass.duration,  \
		timestamp=recordClass.timestamp+interval, timestamp_interval=recordClass.timestamp_interval+interval, \
		timestamp_interval_EST=recordClass.timestamp_interval_EST+interval)
	session.add(new_fare_estimate)
	session.commit()


#Execute#

#interpolateUberXRecords('jb3', 'Buckhead')

#initUberXMeanTable('jb3', 'Buckhead')

#initDayTimeIntervalTable()
