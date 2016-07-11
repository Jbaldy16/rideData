#!/bin/bash

sqlite3 -header -csv RIDEDATA.db "select * from rideData;" > rideData.csv

sqlite3 -header -csv RIDEDATA.db "select * from locations;" > locations.csv