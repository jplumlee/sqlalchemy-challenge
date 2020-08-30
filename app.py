import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
# Import Flask
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the tables
measurement = Base.classes.measurement
station = Base.classes.station

# Creat an app
app = Flask(__name__)

# Home page.
# List all routes that are available.
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>Precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>Stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>TOBS</a><br/>"
        f"<a href='/api/v1.0/<start>'>Start</a><br/>"
        f"<a href='/api/v1.0/<start>/<end>'>Start/End</a><br/>"
    )

# Convert the query results to a dictionary using date as the key and prcp as the value.
@app.route("/api/v1.0/precipitation")
def Precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all precipitation
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= '2016-08-23').all()
    
    session.close()

    # Create a dictionary from the row data and append to a list of all_results
    all_results = []
    for item in results:
        item_dict = {}
        item_dict["date"] = item[0]
        item_dict["prcp"] = item[1]
        all_results.append(item_dict)

    # Return the JSON representation of your dictionary.
    return jsonify(all_results)

# /api/v1.0/stations
@app.route("/api/v1.0/stations")
def Stations():
    session = Session(engine)

    # Query all stations
    results = session.query(station.station).all()

    session.close()

    all_stations = list(np.ravel(results))

# Return a JSON list of stations from the dataset.
    return jsonify(all_stations)

# /api/v1.0/tobs
@app.route("/api/v1.0/tobs")
def TOBS():
    session = Session(engine)
# Query the dates and temperature observations of the most active station for the last year of data.
    results = session.query(measurement.date,measurement.tobs).filter(measurement.date >= '2016-08-23').filter(measurement.station == 'USC00519281').all()
    session.close()

    tobs_results = list(np.ravel(results))
# Return a JSON list of temperature observations (TOBS) for the previous year.
    return jsonify(tobs_results)

# /api/v1.0/<start>
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<start>")
def temperature_start(start):
    session = Session(engine)
# Query the dates and temperature observations    
    results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= '2016-08-23').all()
    
    temperature_start = list(np.ravel(results))
# Return a JSON list of temperature observations (TOBS).
    return jsonify(temperature_start)

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
# /api/v1.0/<start>/<end>
@app.route("/api/v1.0/<start>/<end>")
def temperature_start_end(start, end):
    session = Session(engine)
# Query the dates and temperature observations    
    results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= '2016-08-23').filter(measurement.date <= '2016-08-30').all()
    
    temperature_start_end = list(np.ravel(results))
# Return a JSON list of temperature observations (TOBS).
    return jsonify(temperature_start_end)
if __name__ == "__main__":
    app.run(debug=True)