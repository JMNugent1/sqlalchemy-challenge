import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# create engine to hawaii.sqlite

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model

Base = automap_base()

# reflect the tables

Base.prepare(engine, reflect = True)

# Save references to each table

Measurement = Base.classes.measurement

Station = Base.classes.station

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

previous_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

#################################################
# Flask Routes
#################################################

@app.route("/")
def root():
    return (
                f"/api/v1.0/precipitation<br/>"
                f"/api/v1.0/stations<br/>"
                f"/api/v1.0/tobs<br/>"
                f"/api/v1.0/start<br/>"
                f"/api/v1.0/start/end"
                
            )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Create our session (link) from Python to the DB

    session = Session(engine)

    date_and_prcp = session.query(Measurement.date, Measurement.prcp)\
    .filter(Measurement.date >= previous_year)\
    .all()

    session.close()

    # Create a dictionary from the row data and append to a list

    precipitation_analysis = []
    for date, prcp in date_and_prcp:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation_analysis.append(precipitation_dict)

    return jsonify(precipitation_analysis)

@app.route("/api/v1.0/stations")
def stations():

    # Create our session (link) from Python to the DB

    session = Session(engine)

    all_stations = session.query(Measurement.station)\
    .group_by(Measurement.station)\
    .all()

    session.close()

    # Convert into normal list

    stations_list = list(np.ravel(all_stations))

    #stations_list = [i.station for i in all_stations]

    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():

# Create our session (link) from Python to the DB

    session = Session(engine)

    station_temp = session.query(Measurement.tobs)\
    .filter(Measurement.station == "USC00519281")\
    .filter(Measurement.date >= previous_year)\
    .all()

    session.close()

    # Convert into normal list

    temperature_observations = list(np.ravel(station_temp))

    return jsonify(temperature_observations)

if __name__ == "__main__":
    app.run(debug=True, host = "127.0.0.1", port  = 5000)