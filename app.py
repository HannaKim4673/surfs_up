# Import dependencies
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Sets up and prepares database for future connections
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflects database into classes
Base = automap_base()
Base.prepare(engine, reflect=True)

#Creates references for each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Creates session link
session = Session(engine)

# Creates app Flask instance
app = Flask(__name__)

# Creates Flask routes
# Welcome route
@app.route('/')
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')
# Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
   # Calculates date 1 year ago from most recent database date
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   # Gets date and precipitation for previous year
   precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
   # Creates dictionary with dates as keys and precipitation amounts as values
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)
# Stations route
@app.route("/api/v1.0/stations")
def stations():
    # Gets all stations in database
    results = session.query(Station.station).all()
    # Converts results to list
    stations = list(np.ravel(results))
    return jsonify(stations=stations)
# Monthly Temperature route
@app.route("/api/v1.0/tobs")
def temp_monthly():
    # Calculates date 1 year ago from most recent database date
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Converts results to list
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    # Jsonifies list
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
# Statistics route
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    # Gets descriptive statistics for database
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps=temps)
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)