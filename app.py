#import dependencies

import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#Database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#reflect database and tables
Base=automap_base()
Base.prepare(autoload_with=engine)

#Save references to tables
Measurement = Base.classes.measurement
Station = Base.classes.station

#Flask Setup
app = Flask(__name__)

#Flask Routes

@app.route("/")
def Home():
    return(
        f"Available API Routes:</br>"
        f"/api/v1.0/precipitation</br>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/<start></br>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def Precipitation():
    #create session
    session = Session(engine)    
    #query the data
    data = session.query(Measurement.date,Measurement.prcp).\
        filter(Measurement.date >= '2016-08-23').all()
    session.close()
    #Create empy list, then a for loop with an empty dict.  Append data to dictionary
    prcp_data =[]
    for date,prcp in data:
        prcp_dict = {}
        prcp_dict[date] = prcp
        prcp_data.append(prcp_dict)
    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def Stations():
    #create session
    session = Session(engine) 
    #query the stations
    stations = session.query(Station.name).all()
    session.close()
    #Convert list of tuples to normal list
    all_stations = list(np.ravel(stations))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def Temps():
    #create session
    session = Session(engine)    
    #query the data
    
    temperatures = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date >= '2016-08-23').\
    filter(Measurement.station == 'USC00519281').all()
    #close session
    session.close()
    #Create empy list, then a for loop with an empty dict.  Append data to dictionary
    temp_data =[]
    for date,tobs in temperatures:
        temp_dict = {}
        temp_dict[date] = tobs
        temp_data.append(temp_dict)
    return jsonify(temp_data)

@app.route("/api/v1.0/<start>")
def max_min_avg(start):
    #create session
    session = Session(engine)    
    #query the data

    search_term = session.query(func.max(Measurement.tobs),func.min(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()

    #create list of summary statistics for the search date
    unravled = list(np.ravel(search_term))
    

    return jsonify({"Max": unravled[0]},{"Min": unravled[1]},{"Avg": unravled[2]})


@app.route("/api/v1.0/<start>/<end>")
def max_min_avg_start_end(start,end):
    #create session
    session = Session(engine)    
    #query the data

    search_term = session.query(func.max(Measurement.tobs),func.min(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    #create list of summary statistics for the search date
    unravled = list(np.ravel(search_term))
    
    return jsonify({"Max": unravled[0]},{"Min": unravled[1]},{"Avg": unravled[2]})
   
    
if __name__ == '__main__':
    app.run(debug=True)