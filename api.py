from sqlalchemy import create_engine
from flask import Flask, jsonify
import pandas as pd
import numpy as np


port = 5432
username = "postgres"
password = "postgres"
db_name = "project_db"

# install psycopg2 with "pip install psycopg2" 

# Making connection to postgres database

db_connection_string = f"postgresql+psycopg2://{username}:{password}@localhost:{port}/{db_name}"
engine = create_engine(db_connection_string)

# Creating API

app = Flask(__name__)


@app.route("/")
def homepage():
    #returning information about routes on homepage
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/accident<br/>"
        f"/api/v1.0/person<br/>"
        f"/api/v1.0/vehicle<br/>"
        f"/api/v1.0/counts<br/>"
    )

# This route simply contains data from accident table

@app.route("/api/v1.0/accident")
def accident():
    query = engine.execute('Select * from "accident"')
    accident_list=[]
    for row in query:
        accident_dict={'accident_no':row[0],
                        'date':row[1],
                        'time':row[2],
                        'accident_type':row[3],
                        'day_week_desc':row[4],
                        'light_cond':row[5],
                        'no_persons_killed':row[6],
                        'speed_zone':row[7],
                        'LGA_name':row[8],
                        'region_name':row[9],
                        'DEG_urban_name':row[10],
                        'coordinates':[row[11],row[12]],
                        'atmosph_cond':row[13],
                        'surface_cond':row[14]
                        }
        accident_list.append(accident_dict)
        
    response = jsonify(accident_list)
    response.headers.add('Access-Control-Allow-Origin','*')
    return response

# This route contains data from person dataset

@app.route("/api/v1.0/person")
def person():
    query = engine.execute('Select * from "person"')
    person_list=[]
    for row in query:
        person_dict={'accident_vehicle_id':row[0],
                     'sex':row[1],
                     'age_group':row[2],
                     'road_user_type':row[3]
                    }
        person_list.append(person_dict)
        
    response = jsonify(person_list)
    response.headers.add('Access-Control-Allow-Origin','*')
    return response

@app.route("/api/v1.0/vehicle")
def vehicle():
    query = engine.execute('Select * from "vehicle"')
    vehicle_list=[]
    for row in query:
        vehicle_dict={'accident_vehicle_id':row[0],
                      'vehicle_body_style':row[1],
                      'vehicle_make':row[2],
                      'vehicle_model':row[3],
                      'vehicle_type_desc':row[4]
                      }
        vehicle_list.append(vehicle_dict)
        
    response = jsonify(vehicle_list)
    response.headers.add('Access-Control-Allow-Origin','*')
    return response

# This route contains the number of accidents for each year by feature, e.i the number of accidents by age group in 2016

@app.route("/api/v1.0/counts")
def counts():
    counts_list=[]
    counts_dict={}

    # Finding the counts for each year for each feature
    DEGS = engine.execute('SELECT "DEG_URBAN_NAME","year", COUNT(*) FROM ACCIDENT GROUP BY "DEG_URBAN_NAME","year" ')
    LGA = engine.execute('SELECT "LGA_NAME","year", COUNT(*) FROM ACCIDENT GROUP BY "LGA_NAME","year" ')
    region = engine.execute('SELECT "REGION_NAME","year", COUNT(*) FROM ACCIDENT GROUP BY "REGION_NAME","year"')
    atmos_cond = engine.execute('SELECT "Atmosph_Cond_Desc","year", COUNT(*) FROM ACCIDENT GROUP BY "Atmosph_Cond_Desc","year" ')
    surface_cond = engine.execute('SELECT "Surface_Cond_Desc","year", COUNT(*) FROM ACCIDENT GROUP BY "Surface_Cond_Desc","year" ')
    light_cond = engine.execute('SELECT "Light Condition Desc","year", COUNT(*) FROM ACCIDENT GROUP BY "Light Condition Desc","year" ')
    speed_zone = engine.execute('SELECT "SPEED_ZONE","year", COUNT(*) FROM ACCIDENT GROUP BY "SPEED_ZONE","year" ')
    age_group = engine.execute('SELECT "Age_Group","year", COUNT(*) FROM person GROUP BY "Age_Group","year" ')
    vehicle_type = engine.execute('SELECT "Vehicle Type Desc","year", COUNT(*) FROM vehicle GROUP BY "Vehicle Type Desc","year" ')
    vehicle_brand = engine.execute('SELECT "VEHICLE_MAKE","year", COUNT(*) FROM vehicle GROUP BY "VEHICLE_MAKE","year" ')
                                
    strings=['DEGS','LGA','region','atmos_cond','surface_cond','light_cond','speed_zone','age_group','vehicle_type','vehicle_brand']
    queries = [DEGS,LGA,region,atmos_cond,surface_cond,light_cond,speed_zone,age_group,vehicle_type,vehicle_brand]
    years = [2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020]
    # Creating an array of dictionaries
    for i in range(len(strings)):
        counts_dict[strings[i]] = {}
        count_data = counts_dict[strings[i]]
        for row in queries[i]:
            count_data[f"{row[0]}_{row[1]}"]=row[2]

    counts_list.append(counts_dict)
    response = jsonify(counts_list)
    response.headers.add('Access-Control-Allow-Origin','*')
    return response



if __name__ == '__main__':
    app.run(debug=True)