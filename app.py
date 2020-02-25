from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
app = Flask(__name__)

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

session = Session(engine)
Measurement = Base.classes.measurement
Station = Base.classes.station

results = session.query(Measurement.date).order_by(
    Measurement.date.desc()).first()
date = list(np.ravel(results))[0]


latest_date = dt.datetime.strptime(date, '%Y-%m-%d')

latest_year = int(dt.datetime.strftime(latest_date, '%Y'))

latest_month = int(dt.datetime.strftime(latest_date, '%m'))

latest_day = int(dt.datetime.strftime(latest_date, '%d'))

year_before = dt.date(latest_year, latest_month,
                      latest_day) - dt.timedelta(days=365)

year_before = dt.datetime.strftime(year_before, '%Y-%m-%d')


@app.route("/")
def home():
    return("Hawaii's climate API<br>")
    f"Availabe Routes:<br>"
    f"/api/v1.0/precipitation<br>"
    f"/api/v1.0/stations<br>"
    f"/api/v1.0/tobs<br>"
    f"/api/v1.0/datesearch/2016-08-24/2017-08-23 Low, high, and average temp for date given and each date up to and including end date<br/>"
    f"Data availabe from 2010-01-01 to 2017-08-23<br/>"


@app.route("/api/v1.0/precipitation")
def precipitation():
    prcp_data = session.query(Measurement.date, Measurement.prcp).filter(
        Measurement.date > year_before).order_by(Measurement.date).all()

    precip_data = []
    for result in prcp_data:
        precip_dict = {result.date: result.prcp, "Station": result.station}
        precip_data.append(precip_dict)
    return jsonify(precip_data)


@app.route("/api/v1.0/stations")
def stations():
    station_latest = session.query(Measurement.date, Measurement.tobs).filter(
        Measurement.date > year_before).filter(Measurement.station == station_id).order_by(Measurement.date).all()
    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    tobs = (session.query(Measurement.date, Measurement.tobs, Measurement.station)
            .filter(Measurement.date > year_before)
            .order_by(Measurement.date)
            .all())

    temp_data = []
    for result in tobs:
        temp_dict = {result.date: result.tobs, "Station": result.station}
        temp_data.append(temp_dict)

    return jsonify(temp_data)

    @app.route('/api/v1.0/datesearch/<start_date>')
    def start(start_date):
        sel = [Measurement.date, func.min(Measurement.tobs), func.avg(
            Measurement.tobs), func.max(Measurement.tobs)]

        results = (session.query(*sel).filter(func.starftime("%Y-%m-%d", Measurement.date) >= start_date).filter(
            func.starftime("%Y-%m-%d", Measurement.date) <= end_date).groupby(Measurement.date).all())

    dates = []
    for result in results:
        date_dict = {}
        date_dict["Date"] = result[0]
        date_dict["Low Temp"] = result[1]
        date_dict["Avg Temp"] = result[2]
        date_dict["High Temp"] = result[3]
        dates.append(date_dict)
    return jsonify(dates)


@app.route('/api/v1.0/datesearch/<startDate>/<endDate>')
def start_end(start_date, end_date):
    sel = [Measurement.date, func.min(Measurement.tobs), func.avg(
        Measurement.tobs), func.max(Measurement.tobs)]
    results = (session.query(*sel)
               .filter(func.strftime("%Y-%m-%d", Measurement.date) >= start_date)
               .filter(func.strftime("%Y-%m-%d", Measurement.date) <= end_date)
               .group_by(Measurement.date)
               .all())

    dates = []
    for result in results:
        date_dict = {}
        date_dict["Date"] = result[0]
        date_dict["Low Temp"] = result[1]
        date_dict["Avg Temp"] = result[2]
        date_dict["High Temp"] = result[3]
        dates.append(date_dict)
    return jsonify(dates)


if __name__ == "__main__":
    app.run(debug=True)
