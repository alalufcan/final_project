import os
from flask import Flask, render_template, jsonify
from sqlalchemy import create_engine
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
# Add your Postgres password into the config.py file
# from config import password

app = Flask(__name__)

password="postgres"

# Setup Postgres connection
engine = create_engine(f'postgresql://postgres:{password}@dbname.cxw2xnixkpbl.ca-central-1.rds.amazonaws.com/postgres')


# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
hydro = Base.classes.hydro
weather = Base.classes.weather


# Create the main page
@app.route("/")
def welcome():
    return render_template("index.html")

# Create the Hydro Jsonify Page
@app.route("/api/v1.0/hydro")
def hydrofunc():
    session = Session(engine)
    results = session.query(hydro.date,hydro.hour,hydro.demanded_toronto,hydro.weekday).all()

    session.close()
    
    
    all_hydro = []
    for date, hour, demanded_toronto, weekday in results:
        hydro_dict = {}
        hydro_dict["date"] = date
        hydro_dict["hour"] = hour
        hydro_dict["demanded_toronto"] = demanded_toronto
        hydro_dict["weekday"] = weekday
        all_hydro.append(hydro_dict)

    return jsonify(all_hydro)

# Create the Weather Jsonify Page
@app.route("/api/v1.0/weather")
def weatherfunc():
    session = Session(engine)
    results = session.query(weather.date,weather.hour,weather.dt,weather.timezone,weather.temp,weather.feels_like,weather.temp_min,weather.temp_max,weather.pressure,weather.humidity,weather.wind_speed,weather.wind_deg,weather.clouds_all,weather.weather_main,weather.weather_description).all()

    session.close()
       
    all_weather = []
    for date,hour,dt,timezone,temp,feels_like,temp_min,temp_max,pressure,humidity,wind_speed,wind_deg,clouds_all,weather_main,weather_description in results:
        weather_dict = {}
        weather_dict["date"] = date
        weather_dict["hour"] = hour
        weather_dict["dt"] = dt
        weather_dict["timezone"] = timezone
        weather_dict["temp"] = temp
        weather_dict["feels_like"] = feels_like
        weather_dict["temp_min"] = temp_min
        weather_dict["temp_max"] = temp_max
        weather_dict["pressure"] = pressure
        weather_dict["humidity"] = humidity
        weather_dict["wind_speed"] = wind_speed
        weather_dict["wind_deg"] = wind_deg
        weather_dict["clouds_all"] = clouds_all
        weather_dict["weather_main"] = weather_main
        weather_dict["weather_description"] = weather_description
        all_weather.append(weather_dict)
    
    return jsonify(all_weather)

if __name__ == "__main__":
    app.run(debug=True)