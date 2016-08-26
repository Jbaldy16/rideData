import datetime
from pytz import timezone

def roundTime(dt=None, roundTo=300):
	if dt == None : dt = datetime.datetime.now()
	seconds = (dt - dt.min).seconds
	# // is a floor division, not a comment on following line:
	rounding = (seconds+roundTo/2) // roundTo * roundTo
	return dt + datetime.timedelta(0,rounding-seconds,-dt.microsecond)

def defineUTC(timestamp):
	UTC = timezone('UTC')
	return UTC.localize(timestamp)

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

def getTimeZoneOffset(timeZone):
	today =  datetime.datetime.utcnow()
	loc_timezone = timezone('US/Eastern')
	GMT = timezone('UTC')
	utc_time =  GMT.localize(today)
	timeZoneDelta = loc_timezone.localize(today) - utc_time
	return timeZoneDelta