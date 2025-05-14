import json
import requests
from datetime import datetime, timedelta

# Replace with your valid ThingsBoard Access Token
ACCESS_TOKEN = "4ovbZC1B3L7hZQ2RW6Fk"
THINGSBOARD_URL = f"https://demo.thingsboard.io/api/v1/{ACCESS_TOKEN}/telemetry"

def main():
    try:
        print("📄 Loading sensor_data.json...")
        with open("sensor_data.json", "r") as f:
            data = json.load(f)

        # Get current UTC and convert to Dhaka time (UTC+6)
        utc_now = datetime.utcnow()
        dhaka_now = utc_now + timedelta(hours=6)

        # Floor time to the nearest 10-minute mark
        floored_minute = (dhaka_now.minute // 10) * 10
        floored_time = dhaka_now.replace(minute=floored_minute, second=0, microsecond=0)
        key = floored_time.strftime("%H:%M:%S")

        print(f"⏰ Current Dhaka Time (floored to 10 min): {key}")

        # Check if data exists for this time key
        if key in data:
            payload = data[key]
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
