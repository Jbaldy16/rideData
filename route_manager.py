from database_schema import Routes, session
from utils import getTimeZoneOffset

def addRoute(startLoc, endLoc, routeName, activate=False):
	start_location = session.query(Locations).filter(Locations.name == startLoc).one()
	end_location = session.query(Locations).filter(Locations.name == endLoc).one()
	new_route = Routes(start_location_id=start_location.id, end_location_id=end_location.id, \
		name=routeName, active=activate)
    session.add(new_route)
    session.commit()

def printRoutes():
	routes = session.query(Routes).all()
	for route in routes:
		print 'Route id:', route.id, 'Name:', route.name, 'Active?', route.active

def cycleRoutes():
	pass
