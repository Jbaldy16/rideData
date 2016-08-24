import settings

import datetime
from pytz import timezone

from database_schema_v2 import db_create, db_connect
from database_migration import transferLocations, transferRideData, transferSample

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker


# DataBase Migration Setup
db_transfer_FROM = URL(**settings.AWS_DATABASE)
db_transfer_TO = URL(**settings.AWS_TEST_DATABASE)

databases = [db_transfer_FROM,
    db_transfer_TO]

engines = []
sessions = []
for dbconninfo in databases:
    current_engine = create_engine(dbconninfo)
    engines.append(current_engine)
    sessions.append(sessionmaker(bind=current_engine)())
# End

# Create New Database
#db_create(db_connect(URL(**settings.AWS_TEST_DATABASE)))
# Migrate Data
#transferLocations(sessions)
transferRideData(sessions)
#transferSample(sessions)

print "Success"
# End