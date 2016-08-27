from database_schema import Routes, session
from utils import getTimeZoneOffset

def addRoute(startLoc, endLoc, routeName, activate=False):
	start_location = session.query(Locations).filter(Locations.name == startLoc).one()
	end_location = session.query(Locations).filter(Locations.name == endLoc).one()

	# Check to see if it exists
    check_locs = session.query(exists().where(Routes.start_location_id == start_location.id) \
        .where(Routes.end_location_id == end_location.id).scalar())

    checkname = session.query(exists().where(Routes.name == routeName).scalar())

    if checklocs:
    	print "Route Already Exists"
    	break
    elif checkname:
        print "Route Name Already Used"
    	break
    else:
		new_route = Routes(start_location_id=start_location.id, end_location_id=end_location.id, \
			name=routeName, active=activate)
    	session.add(new_route)
    	session.commit()
    	print "Route Added"

def printRoutes():
	routes = session.query(Routes).all()
	for route in routes:
		print 'Route id:', route.id, 'Name:', route.name, 'Active?', route.active

def activateRoute(routeName=None):
	if routeName==None:
		print "No Route Provided"
		break
	else:
		checkname = session.query(exists().where(Routes.name == routeName).scalar())
		if checkname:
			route = session.query(Routes).filter(Routes.name==routeName).one()
			route.activate = True
			session.commit()

