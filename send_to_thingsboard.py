import json
import requests
from datetime import datetime, timedelta

# Constants
ACCESS_TOKEN = "4ovbZC1B3L7hZQ2RW6Fk"
THINGSBOARD_URL = f"https://demo.thingsboard.io/api/v1/{ACCESS_TOKEN}/telemetry"
WEATHER_API_KEY = "115b9f0d6cc987a7aced5104efcc463a"
CITY = "Rajshahi,BD"
TEMP_ADJUSTMENT = 4.45
DHAKA_UTC_OFFSET = timedelta(hours=6)
REQUEST_TIMEOUT = 5  # seconds

def get_air_temperature():
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&units=metric&appid={WEATHER_API_KEY}"
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        if response.status_code == 200:
            weather = response.json()
            if 'main' in weather and 'temp' in weather['main']:
                air_temp = weather['main']['temp']
                print(f"🌡️ Real-time Air Temp: {air_temp}°C")
                return air_temp
            else:
                raise ValueError("Missing 'main' or 'temp' in weather response.")
        else:
            raise ConnectionError(f"Weather API error: {response.status_code} - {response.text}")
    except Exception as e:
        print("🌐 Failed to fetch weather data.")
        print(e)
        return None

def load_sensor_data():
    try:
        print("📄 Loading sensor_data.json...")
        with open("sensor_data.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ sensor_data.json not found.")
    except json.JSONDecodeError as e:
        print("❌ Failed to decode JSON file.")
        print(e)
    return None

def get_floored_dhaka_time_key():
    utc_now = datetime.utcnow()
    dhaka_now = utc_now + DHAKA_UTC_OFFSET
    floored_minute = (dhaka_now.minute // 10) * 10
    floored_time = dhaka_now.replace(minute=floored_minute, second=0, microsecond=0)
    key = floored_time.strftime("%H:%M:%S")
    print(f"⏰ Current Dhaka Time (floored to 10 min): {key}")
    return key

def send_to_thingsboard(payload):
    try:
        headers = {"Content-Type": "application/json"}
        response = requests.post(THINGSBOARD_URL, json=payload, headers=headers, timeout=REQUEST_TIMEOUT)
        if response.status_code == 200:
            print(f"✅ Data sent to ThingsBoard: {response.status_code} - {response.text}")
        else:
            print("❌ Failed to send data to ThingsBoard.")
            print(f"Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print("🚨 Error sending data to ThingsBoard:")
        print(e)

def main():
    data = load_sensor_data()
    if not data:
        return

    key = get_floored_dhaka_time_key()
    if key not in data:
        print(f"⚠️ No data available for key: {key}")
        return

    payload = data[key]

    air_temp = get_air_temperature()
    if air_temp is not None:
        water_temp = round(air_temp - TEMP_ADJUSTMENT, 1)
        payload['temperature'] = water_temp
        print(f"💧 Adjusted Water Temp (Air - {TEMP_ADJUSTMENT}°C): {water_temp}°C")
    else:
        print("⚠️ Skipping temperature injection due to API error.")
        return

    print(f"📤 Sending payload to ThingsBoard: {payload}")
    send_to_thingsboard(payload)

if __name__ == "__main__":
    main()
