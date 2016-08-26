import settings
from uber_rides.session import Session
from uber_rides.client import UberRidesClient

def requestUberData(strService, Lat1, Long1, Lat2, Long2):
	session = Session(server_token=settings.UBER_SERVER_TOKEN)
	client = UberRidesClient(session)
	response = client.get_price_estimates(Lat1, Long1, Lat2, Long2)
	prices = response.json.get('prices')

	uberData = {}
	uberService = []

	for service in prices:
		if service['localized_display_name'] == strService:
			uberService = service

	if not uberService:
		print "Incorrect Uber Service Requested"
	else:
		highEstimate = float(uberService['high_estimate'])
		lowEstimate = float(uberService['low_estimate'])
		distance = float(uberService['distance'])
		duration = float(uberService['duration'])
		surge = float(uberService['surge_multiplier'])

		if strService != "POOL":
			minimum = float(uberService['minimum'])
			estimate = None
		else:
			minimum = None
			estimate = float(uberService['estimate'][1:])

		uberData = {'highEstimate': highEstimate, 'lowEstimate': lowEstimate, \
			'minimum': minimum, 'estimate': estimate, 'distance': distance, \
			'duration': duration, 'surge': surge}

	return uberData