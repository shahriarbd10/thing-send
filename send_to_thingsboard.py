import json
import requests
from datetime import datetime, timedelta

# Replace with your valid ThingsBoard Access Token
ACCESS_TOKEN = "4ovbZC1B3L7hZQ2RW6Fk"
THINGSBOARD_URL = f"https://demo.thingsboard.io/api/v1/{ACCESS_TOKEN}/telemetry"
WEATHER_API_KEY = "115b9f0d6cc987a7aced5104efcc463a"  # Replace with your API key
CITY = "Rajshahi,BD"

def get_air_temperature():
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&units=metric&appid={WEATHER_API_KEY}"
        response = requests.get(url)
        weather = response.json()
        air_temp = weather['main']['temp']
        print(f"🌡️ Real-time Air Temp: {air_temp}°C")
        return air_temp
    except Exception as e:
        print("🌐 Failed to fetch weather data.")
        print(e)
        return None

def main():
    try:
        print("📄 Loading sensor_data.json...")
        with open("sensor_data.json", "r") as f:
            data = json.load(f)

        # Calculate current Dhaka time floored to the last 10-minute mark
        utc_now = datetime.utcnow()
        dhaka_now = utc_now + timedelta(hours=6)
        floored_minute = (dhaka_now.minute // 10) * 10
        floored_time = dhaka_now.replace(minute=floored_minute, second=0, microsecond=0)
        key = floored_time.strftime("%H:%M:%S")

        print(f"⏰ Current Dhaka Time (floored to 10 min): {key}")

        if key in data:
            payload = data[key]

            # Always override temperature with 2.5°C less than current air temp
            air_temp = get_air_temperature()
            if air_temp is not None:
                water_temp = round(air_temp - 5.85, 1)
                payload['temperature'] = water_temp
                print(f"💧 Adjusted Water Temp (Air - 5.85°C): {water_temp}°C")
            else:
                print("⚠️ Skipping temperature injection due to API error.")
                return

            print(f"📤 Sending payload to ThingsBoard: {payload}")
            headers = {"Content-Type": "application/json"}
            response = requests.post(THINGSBOARD_URL, json=payload, headers=headers)
            print(f"✅ Response: {response.status_code} - {response.text}")
        else:
            print(f"⚠️ No data available for key: {key}")

    except Exception as e:
        print("🚨 An error occurred:")
        print(e)

if __name__ == "__main__":
    main()
