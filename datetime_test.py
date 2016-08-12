import datetime
from pytz import timezone

import database_schema

from sqlalchemy import create_engine, exists
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL

engine = create_engine(URL(**settings.AWS_TEST_DATABASE))
 
DBSession = sessionmaker(bind=engine)
session = DBSession()