from flask import Flask, render_template, request
import requests
from datetime import datetime, timedelta


today = datetime.now().strftime("%Y-%m-%d")
app = Flask(__name__)



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/history")
def history():
    return render_template("history.html")


@app.route("/search", methods=['POST', 'GET'])
def search():
    # Step 1: Get place from form
    place_name = request.form.get('search', '').strip()
    
    

    # Step 2: Get location details from Open-Meteo geocoding API
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={place_name}&count=1&country_code=IN"
    geo_response = requests.get(geo_url)
    geo_data = geo_response.json()

    

    location = geo_data["results"][0]

    # Extract location details
    lat = location.get("latitude")
    lon = location.get("longitude")
    elevation = location.get("elevation", "Not Available")
    state = location.get("admin1", "Not Available")
    district = location.get("admin2", "Not Available")
    sub_district = location.get("admin3", "Not Available")
    country = location.get("country", "Unknown")

    # Step 3: Date range (last 3 days)
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=3)

    # Step 4: Fetch weather history
    weather_url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={lon}"
        f"&start_date={start_date}&end_date={end_date}"
        f"&hourly=rain,relative_humidity_2m,soil_moisture_0_to_7cm"
    )
    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()

    # Extract hourly data
    hourly_rain = weather_data["hourly"].get("rain", [])
    humidity = weather_data["hourly"].get("relative_humidity_2m", [])
    soil_moisture = weather_data["hourly"].get("soil_moisture_0_to_7cm", [])

    # Step 5: Calculate features
    rainfall_last_24h = sum(hourly_rain[-24:]) if len(hourly_rain) >= 24 else sum(hourly_rain)
    rainfall_last_3_days = sum(hourly_rain)
    avg_humidity = sum(humidity[-24:]) / 24 if len(humidity) >= 24 else sum(humidity) / max(len(humidity), 1)
    avg_soil_moisture = sum(soil_moisture[-24:]) / 24 if len(soil_moisture) >= 24 else sum(soil_moisture) / max(len(soil_moisture), 1)


    # Step 6: Pass values to template
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
        mois=round(avg_soil_moisture, 4)
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)