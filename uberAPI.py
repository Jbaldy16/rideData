import settings
from uber_rides.session import Session
from uber_rides.client import UberRidesClient

def requestUberData(strService, Lat1, Long1, Lat2, Long2):
	session = Session(server_token=settings.UBER_SERVER_TOKEN)
	client = UberRidesClient(session)
	response = client.get_price_estimates(Lat1, Long1, Lat2, Long2)
	prices = response.json.get('prices')

	uberData = {}

	if strService == "uberPOOL":
		uberService = prices[0]
	elif strService == "uberX":
		uberService = prices[1]
	elif strService == "uberXL":
		uberService = prices[2]
	elif strService == "uberSELECT":
		uberService = prices[3]
	elif strService == "uberBLACK":
		uberService = prices[4]
	elif strService == "uberSUV":
		uberService = prices[5]
	else:
		print "Incorrect Uber Service Requested"

	highEstimate = float(uberService['high_estimate'])
	lowEstimate = float(uberService['low_estimate'])
	distance = float(uberService['distance'])
	surge = float(uberService['surge_multiplier'])

	if strService != "uberPOOL":
		minimum = float(uberService['minimum'])
		estimate = None
	else:
		minimum = None
		estimate = float(uberService['estimate'][1:])

	uberData = {'highEstimate': highEstimate, 'lowEstimate': lowEstimate, \
		'minimum': minimum, 'estimate': estimate, 'distance': distance, 'surge': surge}

	return uberData