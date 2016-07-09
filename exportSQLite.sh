#!/bin/bash

sqlite3 -header -csv RIDEDATA.db "select * from SurgePrices;" > out.csv