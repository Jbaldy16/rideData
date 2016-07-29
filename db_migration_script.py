import settings

from database_schema_v2 import db_create, db_connect
from database_migration import transferLocations, transferRideData
from database_cleanup import updateDateTime, addRoundedTime

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

# DataBase Cleanup Setup
db_TO_BE_CLEANED = URL(**settings.AWS_DATABASE)

engine = create_engine(db_TO_BE_CLEANED)
session = sessionmaker(bind=engine)()
# End

# DataBase Migration Setup
db_transfer_FROM = 'sqlite:///RIDEDATA.db'
db_transfer_TO = URL(**settings.AWS_DATABASE)

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
db_create(db_connect(URL(**settings.AWS_DATABASE)))
# Migrate Data
#transferLocations(sessions)
#transferRideData(sessions)
# Cleanup Data
#updateDateTime(session)
#addRoundedTime(session)
print "Success"

# End