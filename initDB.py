import settings

import datetime
from pytz import timezone

from database_cleanup import roundTime, defineUTC
from database_schema import session, DayTimeIntervals, UberXMedian, UberXData, Locations, RideData

from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL

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

def initUberXMedianTable(startLoc, endLoc):
	start_location = session.query(Locations).filter(Locations.name == startLoc).one()
	end_location = session.query(Locations).filter(Locations.name == endLoc).one()

	uberX_records = DBsession.query(UberXData).filter(UberXData.start_location_id==start_location.id). \
		filter(UberXData.end_location_id==end_location.id)

	for uberXEntry in uberX_records:
		time_interval = uberXEntry.timestamp_interval_EST
		weekday_index = time_interval.weekday()
		time = time_interval.time()

		dayTimeInterval_record = DBsession.query(DayTimeIntervals).filter(DayTimeIntervals.day_index==weekday_index). \
			filter(DayTimeIntervals.time_interval==time).first()

		uberXMedian_record = DBsession.query(UberXMedian).filter(UberXMedian.day_time_interval_id==dayTimeInterval_record.id). \
			filter(UberXMedian.start_location_id==start_location.id). \
			filter(UberXMedian.end_location_id==end_location.id).first()

		if uberXMedian_record == None:
			# No current Median records exists for that timestamp and route
			new_uberX_median = UberXMedian(start_location_id=start_location.id, end_location_id=end_location.id, \
			surge=uberXEntry.surge, highEstimate=uberXEntry.highEstimate, lowEstimate=uberXEntry.lowEstimate, \
			minimum=uberXEntry.minimum, distance=uberXEntry.distance, duration=uberXEntry.duration,  \
			day_time_interval_id= dayTimeInterval_record.id, data_points=1 )
			session.add(new_uberX_median)
			session.commit()
			print 'Added New Record'
		else:
			# Update Surge
			uberXMedian_record.surge = averageData(uberXMedian_record.surge, uberXMedian_record.data_points, uberXEntry.surge)
			session.commit()
			# Update highEstimate
			uberXMedian_record.highEstimate = averageData(uberXMedian_record.highEstimate, uberXMedian_record.data_points, uberXEntry.highEstimate)
			session.commit()
			# Update lowEstimate
			uberXMedian_record.lowEstimate = averageData(uberXMedian_record.lowEstimate, uberXMedian_record.data_points, uberXEntry.lowEstimate)
			session.commit()
			# Update Minimum
			uberXMedian_record.minimum = averageData(uberXMedian_record.minimum, uberXMedian_record.data_points, uberXEntry.minimum)
			session.commit()
			# Update Distance
			uberXMedian_record.distance = averageData(uberXMedian_record.distance, uberXMedian_record.data_points, uberXEntry.distance)
			session.commit()
			# Update Duration
			uberXMedian_record.duration = averageData(uberXMedian_record.duration, uberXMedian_record.data_points, uberXEntry.duration)
			session.commit()
			# Update Data Points
			uberXMedian_record.data_points = uberXMedian_record.data_points + 1
			print 'Updated Record'


def averageData(cur_average, cur_data_points, new_value):
		if cur_average == None and new_value == None:
			return None
		elif new_value == None:
			return cur_average
		elif cur_average == None:
			return new_value
		else:
			current_sum = cur_average * cur_data_points
			new_sum = current_sum + new_value
			new_data_points = cur_data_points + 1
			new_average = new_sum / new_data_points
			return new_average

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

interpolateUberXRecords('jb3', 'Buckhead')

#initUberXMedianTable(session, 'jb3', 'Buckhead')

#initDayTimeIntervalTable(session)

#today = datetime.datetime.now()
#print today.weekday()
#print today.time()