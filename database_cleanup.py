
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
