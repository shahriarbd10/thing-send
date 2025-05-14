import json
import requests
from datetime import datetime, timedelta  # ✅ FIXED: added timedelta


ACCESS_TOKEN = "4ovbZC1B3L7hZQ2RW6Fk"
THINGSBOARD_URL = f"https://demo.thingsboard.io/api/v1/{ACCESS_TOKEN}/telemetry"

def main():
    try:
        print("📄 Loading sensor_data.json...")
        with open("sensor_data.json", "r") as f:
            data = json.load(f)

        # Get current UTC time and convert it to Dhaka time (UTC+6)
        utc_now = datetime.utcnow()
        dhaka_now = utc_now + timedelta(hours=6)  # Adjust to Dhaka time (UTC+6)

        # Floor to the nearest 10-minute mark
        floored_minute = (dhaka_now.minute // 10) * 10
        floored_time = dhaka_now.replace(minute=floored_minute, second=0, microsecond=0)
        key = floored_time.strftime("%H:%M:%S")

        print(f"⏰ Dhaka time (UTC+6) floored to 10 mins: {key}")

        # Check if key exists in the data and send it to ThingsBoard
        if key in data:
            payload = data[key]
            print(f"📤 Sending to ThingsBoard: {payload}")
            response = requests.post(THINGSBOARD_URL, json=payload)
            print(f"✅ Status code: {response.status_code}")
            print(f"📝 Response text: {response.text}")
        else:
            print(f"⚠️ No data available for key: {key}")

    except Exception as e:
        print("🚨 An error occurred:")
        print(e)
        exit(2)

if __name__ == "__main__":
    main()