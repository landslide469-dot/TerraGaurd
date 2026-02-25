from flask import Flask, render_template, request
import requests
from datetime import datetime, timedelta
import sqlite3
import random
import dataBase as db
import userData as usrDb

# Initialize Flask app
app = Flask(__name__)

# Current date (not used in search but kept)
today = datetime.now().strftime("%Y-%m-%d")


# ------------------ ROUTES ------------------

@app.route("/")
def index():
    # Home page
    return render_template("index.html")


@app.route("/contact")
def contact():
    # Contact page
    return render_template("contact.html")


@app.route("/history")
def history():
    # History page
    return render_template("history.html")



@app.route("/search", methods=['POST', 'GET'])
def search():

    place_name = request.form.get('search', '').strip()

    if not place_name:
        return render_template("search.html")

    # -------------------------------------------------
    # SEARCH USING AREA CODE
    # -------------------------------------------------
    if place_name.isnumeric():

        coords = db.get_user_area_by_code(place_name)

        if not coords:
            return render_template("search.html", error="Invalid Area Code")

        lat, lon = coords
        area_code = place_name

    # -------------------------------------------------
    # SEARCH USING PLACE NAME
    # -------------------------------------------------
    else:

        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={place_name}&count=1&country_code=IN"
        geo_response = requests.get(geo_url)
        geo_data = geo_response.json()

        if "results" not in geo_data:
            return render_template("search.html", error="Place not found")

        location = geo_data["results"][0]
        lat = location["latitude"]
        lon = location["longitude"]

        # Check if already exists
        existing_code = db.get_area_by_coordinates(lat, lon)

        if existing_code:
            area_code = existing_code
        else:
            area_code = db.insert_user_area(
                name="DefaultUser",
                mobile="0000000000",
                risk_rate="Low",
                disaster="None",
                latitude=lat,
                longitude=lon
            )

    # -------------------------------------------------
    # FETCH WEATHER DATA
    # -------------------------------------------------
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=3)

    weather_url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={lon}"
        f"&start_date={start_date}&end_date={end_date}"
        f"&hourly=rain,relative_humidity_2m,soil_moisture_0_to_7cm"
    )

    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()

    hourly_rain = weather_data.get("hourly", {}).get("rain", [])
    humidity = weather_data.get("hourly", {}).get("relative_humidity_2m", [])
    soil_moisture = weather_data.get("hourly", {}).get("soil_moisture_0_to_7cm", [])

    rainfall_last_24h = sum(hourly_rain[-24:])
    rainfall_last_3_days = sum(hourly_rain)

    avg_humidity = sum(humidity[-24:]) / 24 if humidity else 0
    avg_soil_moisture = sum(soil_moisture[-24:]) / 24 if soil_moisture else 0

    return render_template(
        "search.html",
        rainfall_24=round(rainfall_last_24h, 2),
        rainfall_3days=round(rainfall_last_3_days, 2),
        humi=round(avg_humidity, 2),
        mois=round(avg_soil_moisture, 4),
        city=place_name,
        area_code=area_code
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