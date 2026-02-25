import requests
from datetime import datetime, timedelta

# Step 1: Get city name
city = input("Enter city name: ")

# Step 2: Get location details
geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"

geo_response = requests.get(geo_url)
geo_data = geo_response.json()

if "results" not in geo_data:
    print("City not found")
    exit()

location = geo_data["results"][0]

lat = location["latitude"]
lon = location["longitude"]
elevation = location["elevation"]

state = location.get("admin1", "Not Available")
district = location.get("admin2", "Not Available")
sub_district = location.get("admin3", "Not Available")
country = location.get("country", "Unknown")

print("\n--- Location Details ---")
print("Country:", country)
print("State:", state)
print("District:", district)
print("Sub-District:", sub_district)
print("Latitude:", lat)
print("Longitude:", lon)
print("Elevation:", elevation, "m")

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

hourly_rain = weather_data["hourly"]["rain"]
humidity = weather_data["hourly"]["relative_humidity_2m"]
soil_moisture = weather_data["hourly"]["soil_moisture_0_to_7cm"]

# Step 5: Calculate features
rainfall_last_24h = sum(hourly_rain[-24:])
rainfall_last_3_days = sum(hourly_rain)

avg_humidity = sum(humidity[-24:]) / 24
avg_soil_moisture = sum(soil_moisture[-24:]) / 24

# Step 6: Print ML Features
print("\n--- Landslide Features ---")
print("Rainfall Last 24h:", round(rainfall_last_24h, 2), "mm")
print("Rainfall Last 3 Days:", round(rainfall_last_3_days, 2), "mm")
print("Average Humidity (24h):", round(avg_humidity, 2), "%")
print("Average Soil Moisture (24h):", round(avg_soil_moisture, 4))