from flask import Flask, jsonify
import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()

Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def welcome():
    return (
        f"Welcome API!<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp_with_start_date:yyyy-mm-dd/<s_date><br/>"
        f"/api/v1.0/temp_with_start_and_end_date:yyyy-mm-dd/<s_dates>/<e_date><br/>"
    )
##################################################    
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
                        
    rain_days = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date == date).all()
    session.close()
    
    date_prec = []
    for date, precipitation in rain_days:
        rain_days_dict = {}
        rain_days["date"] = date
        rain_days["precipitation"] = precipitation
        date_prec.append(rain_days_dict)

    return jsonify(date_prec)
##################################################    
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stationlist = session.query(Station.station, Station.name).all()

    session.close()

    return jsonify(stationlist)
##################################################    
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    temp_obs = session.query(Measurement.date,  Measurement.tobs).filter(Measurement.date >= '2016-08-23').order_by(Measurement.date).all()
    session.close()
    temp_obs_list = []
    for date, temp in temp_obs:
        temp_obs_dict = {}
        temp_obs_dict["date"] = date
        temp_obs_dict["temperature"] = temp
        temp_obs_list.append(temp_obs_dict)

    return jsonify(temp_obs_list)
##################################################    
@app.route("/api/v1.0/temp_with_start_date:yyyy-mm-dd/<s_date>")
def temp_with_start_date(s_date):
    session = Session(engine)
    temp_start_date_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= s_date).all()
    session.close()
    return jsonify(temp_start_date_query)

##################################################  
@app.route("/api/v1.0/temp_with_start_and_end_date:yyyy-mm-dd/<s_date>/<e_date>")
def temp_sdate_edate(s_dates, e_date):
 
    session = Session(engine)
    temp_sdate_edate_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= s_date).filter(Measurement.date <= e_date).all()

    session.close()

    return jsonify(temp_sdate_edate_query)

if __name__ == '__main__':
    app.run(debug=True)
