# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite://Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
station = Base.classes.station
measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Welcome to my Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>")

@app.route("/api/v1.0/precipitation")
def Percipitation():
    session = Session(engine)
    recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    query = session.query(measurement.date, measurement.prcp).filter(measurement.date >= year_ago).all()
    prcp_data = {date:prcp for date, prcp in query}
    return jsonify(percipitation_data)

@app.route("/api/v1.0/stations")
def Stations():
    session = Session(engine)
    results = session.query(station.station).all()
    station_list = list(np.ravel(results))
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def Tobs():
    session = Session(engine)
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    station_counts = session.query(measurement.station, func.count(measurement.station))
    grouped = station_counts.group_by(measurement.station)
    ordered = grouped.order_by(func.count(measurement.station).desc()).all()
    most_active = ordered[0][0]
    query = session.query(measurement.tobs).filter(measurement.station == most_active).filter(measurement.date >= year_ago).all()
    tops_ordered = session.query(measurement.tobs).order_by(measurement.date.desc()).all()
    return jsonify(tobs_ordered)

@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def Dynamic_Temp_Stats(start, end=None):
    session = Session(engine)
    start_date = dt.datetime.strptime(start, '%Y-%m-%d').date()
    if end:
        end_date = dt.datetime.strptime(end, '%Y-%m-%d').date()
    else:
        end_date = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
    results = session.query(func.min(measurement.tobs),func.avg(measurement.tobs),func.max(measurement.tobs).\
                            filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
    temp_stats = [{'Min Temp': tmin, 'Avg Temp': tavg, 'Max Temp': tmax} for tmin, tavg, tmax in results]
    return jsonify(temp_stats)
                            
if __name__ == '__main__':
    app.run(debug=True)