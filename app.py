import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

base = automap_base()
base.prepare(engine, reflect=True)
measurement = base.classes.measurement
station = base.classes.station
session = Session(engine)

app = Flask(__name__)


@app.route("/")
def home():
    return ('<a href="/api/v1.0/precipitation">Rain</a><br><a href="/api/v1.0/stations">Stations</a><br><a href="/api/v1.0/tobs">Temps</a><br><a href="/api/v1.0/temp/<start>/<end>">Temp Info</a><br>')
    
@app.route("/api/v1.0/precipitation")
def rain():

    yr = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    rain = session.query(measurement.date, measurement.prcp).filter(measurement.date >= yr).all()
    rn = {date: prcp for date, prcp in rain}
    return jsonify(rn)


@app.route("/api/v1.0/stations")
def stations():
    results = session.query(station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)


@app.route("/api/v1.0/tobs")
def temps():
    yr = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temps = session.query(measurement.tobs).filter(measurement.station == 'USC00519281').filter(measurement.date >= yr).all()
    temp_list = list(np.ravel(temps))
    return jsonify(temps=temp_list)


@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]

    if not end:
        data = session.query(*sel).filter(measurement.date >= start).all()
        temps = list(np.ravel(data))
        return jsonify(temps)

    temps = session.query(*sel).filter(measurement.date >= start).filter(Measurement.date <= end).all()
    temp_list = list(np.ravel(temps))
    return jsonify(temps=temp_list)


if __name__ == '__main__':
    app.run()
