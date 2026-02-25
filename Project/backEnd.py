from flask import Flask, render_template, request
import requests
from datetime import datetime, timedelta
import sqlite3
import random
import dataBase as db
import userData as usrDb
import terraGaurdDB as MainDB
import joblib
import pandas as pd

# Initialize Flask app
app = Flask(__name__)

# Current date (not used in search but kept)
today = datetime.now().strftime("%Y-%m-%d")

model = joblib.load("terraModel.pkl")

# ------------------ ROUTES ------------------

@app.route("/")
def index():
    # Home page
    return render_template("index.html")


@app.route("/contact")
def contact():
    # Contact page
    
    name = "HFOIUWYFW"
    mobile = "7856384"
    password = "8987"
    
    MainDB.create_new_user(name,mobile,password)
    
    return render_template("contact.html")


@app.route("/history")
def history():
    # History page
    
    #mobile = '11111'
   # password = '00000'
    
    
   # MainDB.fetch_user(mobile,password)
    
    
    return render_template("history.html")


@app.route("/search", methods=['POST', 'GET'])
def search():
    # ------------------ Step 1: Get place from form ------------------
    place_name = request.form.get('search', '').strip()
    
    
    # If no city entered, render template without results
    if not place_name:
        return render_template("search.html")










#IF AREA CODE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if place_name.isnumeric():
          
       area = MainDB.fetchAreaTableByCode(place_name)
       
       lat,long = area
       
       print("LATT : ",lat,"LONG  : ",long)
       
        # ------------------ Step 2: Get location details from Open-Meteo ------------------
       geo_url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={long}&format=json"
       geo_response = requests.get(geo_url,headers={"User-Agent": "my_app"})
       
       geo_data = geo_response.json()
       
       
       
       
       

    # ------------------ Step 3: Validate API results ------------------
       if  not geo_data:
           return render_template("search.html", error=f"Area Code '{place_name}' not found")

       

    # ------------------ Step 4: Extract location info ------------------
       
      # elevation = geo_data["address"].get("elevation", "Not Available")
       state = geo_data["address"].get("state", "Not Available")
       district = geo_data["address"].get("state_district", "Not Available")
       sub_district = geo_data["address"].get("town", "Town Not Available")
       country = geo_data["address"].get("country", "Unknown")
       
       #geo_url_forElevation = (f"https://geocoding-api.open-meteo.com/v1/search?"f"name={sub_district}&count=1&country_code=IN")
       
       #geo_url_forElevation = f"https://geocoding-api.open-meteo.com/v1/search?name={state|district|sub_district}&count=1&country_code=IN"
      # geo_response_forElevation = requests.get(geo_url_forElevation)
      # geo_data_forElevation = geo_response_forElevation.json()

    # ------------------ Step 5: Define date range (last 3 days) ------------------
       end_date = datetime.today().date()
       start_date = end_date - timedelta(days=3)

    # ------------------ Step 6: Fetch weather history ------------------
       weather_url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={long}"
        f"&start_date={start_date}&end_date={end_date}"
        f"&hourly=rain,relative_humidity_2m,soil_moisture_0_to_7cm"
    )
       weather_response = requests.get(weather_url)
       weather_data = weather_response.json()

    # ------------------ Step 7: Extract hourly data safely ------------------
       hourly_rain = weather_data.get("hourly", {}).get("rain", [])
       humidity = weather_data.get("hourly", {}).get("relative_humidity_2m", [])
       soil_moisture = weather_data.get("hourly", {}).get("soil_moisture_0_to_7cm", [])
       
       #NewElevation = geo_data_forElevation["results"][0]
       
       elevation = '200' #NewElevation.get("elevation", "Unknown")
    # ------------------ Step 8: Calculate features ------------------
       rainfall_last_24h = sum(hourly_rain[-24:]) if len(hourly_rain) >= 24 else sum(hourly_rain)
       rainfall_last_3_days = sum(hourly_rain)
       avg_humidity = sum(humidity[-24:]) / 24 if len(humidity) >= 24 else sum(humidity) / max(len(humidity), 1)
       avg_soil_moisture = sum(soil_moisture[-24:]) / 24 if len(soil_moisture) >= 24 else sum(soil_moisture) / max(len(soil_moisture), 1)

     
        
    #-------- INSERTING UNIQUE AREA CODE AND PLACE NAME -------
       name = 'ZERRERRERE'
       mobile = "1111111"
       password = "12345"
       risk_rate = "91.5%"
       disaster = "Flood"
       latitude = geo_data.get("lat", "Not Available")
       longitude = geo_data.get("lon", "Not Available")
    
       #area_code = db.generate_unique_code(place_name)
       
       #if area_code:
          # print(name,"\n",mobile)

       #db.create_area_table(name,mobile,risk_rate,disaster,latitude,longitude)
    
       
    
       ##usrDb.insert_new_user(name,mobile,password)
    
    #print("Area Code -> ",db.get_user_area(latitude,longitude))

        
           
           
       return render_template(
        "search.html",
            state=state,
            district=district,
           sub_district=sub_district,
            country=country,
           elevation=elevation,
           rainfall_24=round(rainfall_last_24h, 2),
            rainfall_3days=round(rainfall_last_3_days, 2),
           humi=round(avg_humidity, 2),
           mois=round(avg_soil_moisture, 4),
            city=place_name,
           area_code = place_name
    )

#IF AREA CODE END %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%












    if type(place_name==str):
    
       
       
        
    
       MainDB.create_area_table()
    # ------------------ Step 2: Get location details from Open-Meteo ------------------
       geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={place_name}&count=1&country_code=IN"
       geo_response = requests.get(geo_url)
       geo_data = geo_response.json()

    # ------------------ Step 3: Validate API results ------------------
       if "results" not in geo_data or len(geo_data["results"]) == 0:
           return render_template("search.html", error=f"City ' {place_name} ' not found")

       location = geo_data["results"][0]

    # ------------------ Step 4: Extract location info ------------------
       lat = location.get("latitude")
       lon = location.get("longitude")
       elevation = location.get("elevation", "Not Available")
       state = location.get("admin1", "Not Available")
       district = location.get("admin2", "Not Available")
       sub_district = location.get("admin3", "Not Available")
       country = location.get("country", "Unknown")

       print("LAT : ",lat,"\n","LONG : ",lon)

    # ------------------ Step 5: Define date range (last 3 days) ------------------
       end_date = datetime.today().date()
       start_date = end_date - timedelta(days=3)

    # ------------------ Step 6: Fetch weather history ------------------
       weather_url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={lon}"
        f"&start_date={start_date}&end_date={end_date}"
        f"&hourly=rain,relative_humidity_2m,soil_moisture_0_to_7cm"
    )
       weather_response = requests.get(weather_url)
       weather_data = weather_response.json()

    # ------------------ Step 7: Extract hourly data safely ------------------
       hourly_rain = weather_data.get("hourly", {}).get("rain", [])
       humidity = weather_data.get("hourly", {}).get("relative_humidity_2m", [])
       soil_moisture = weather_data.get("hourly", {}).get("soil_moisture_0_to_7cm", [])

    # ------------------ Step 8: Calculate features ------------------
       rainfall_last_24h = sum(hourly_rain[-24:]) if len(hourly_rain) >= 24 else sum(hourly_rain)
       rainfall_last_3_days = sum(hourly_rain)
       avg_humidity = sum(humidity[-24:]) / 24 if len(humidity) >= 24 else sum(humidity) / max(len(humidity), 1)
       avg_soil_moisture = sum(soil_moisture[-24:]) / 24 if len(soil_moisture) >= 24 else sum(soil_moisture) / max(len(soil_moisture), 1)

       #area_code = db.get_user_area(lat,lon)
       
        #-------- INSERTING UNIQUE AREA CODE AND PLACE NAME -------
       #-------- INSERTING UNIQUE AREA CODE AND PLACE NAME -------
       
       
    
    
       #usrDb.create_new_user_table(name,mobile,password)
       #usrDb.insert_new_user(name,mobile,password)
    
       #area_code = db.generate_unique_code()
       

      # Prepare features
       humModel = round(avg_humidity, 2)
       moiModel = round(avg_soil_moisture, 4)
       rain24   = round(rainfall_last_24h, 2)
       rain3day = round(rainfall_last_3_days, 2)
       eleModel = round(elevation, 2)

       samples = [[humModel, rain24, rain3day, moiModel, eleModel]]

# Predict class
       predicted_class = model.predict(samples)[0]

# Predict probability of predicted class
       predicted_prob = max(model.predict_proba(samples)[0])  # highest probability
       pred_percent = round(predicted_prob * 100, 2)

       print(predicted_class, pred_percent, "%")

       
       name = "NEW USER"
       mobile = "NEW MOBILE"
       
       
       
       
       
       insert = MainDB.insert_user_area(name,mobile,pred_percent,predicted_class,lat, lon)
       
       if insert:
           print("QUERY RINNING....")
           
           #fetch = MainDB.get_user_area(code)
       
       #db.create_area_table(area_code,name,mobile,risk_rate,disaster,latitude,longitude)
       
       
       
       area_code = MainDB.fetchAreaTable(lat,lon) 
    
    return render_template(
        "search.html",
            state=state,
            district=district,
           sub_district=sub_district,
            country=country,
           elevation=elevation,
           rainfall_24=round(rainfall_last_24h, 2),
            rainfall_3days=round(rainfall_last_3_days, 2),
            
           humi=round(avg_humidity, 2),
           mois=round(avg_soil_moisture, 4),
            city=place_name,
            area_code = area_code[0],
            risk = predicted_class,
            proba = pred_percent
    )

   


@app.route("/settings")
def settings():
    return render_template("settings.html")


@app.route("/shelter")
def shelter():
    return render_template("shelter.html")


@app.route("/warning")
def warning():
    return render_template("warning.html")


# ------------------ RUN APP ------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)