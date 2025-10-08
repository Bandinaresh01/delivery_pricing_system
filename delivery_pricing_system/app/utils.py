import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config

def get_distance(origin, destination):
    """
    Calculate distance using Google Maps Directions API.
    Returns distance in km.
    For demo, return mock distance.
    """
    # Mock for demo
    return 12.5  # km
    # Uncomment below for real API
    # url = "https://maps.googleapis.com/maps/api/directions/json"
    # params = {
    #     "origin": origin,
    #     "destination": destination,
    #     "key": Config.GOOGLE_MAPS_API_KEY
    # }
    # response = requests.get(url, params=params)
    # data = response.json()
    # if data["status"] == "OK":
    #     distance_meters = data["routes"][0]["legs"][0]["distance"]["value"]
    #     return distance_meters / 1000  # km
    # else:
    #     raise Exception(f"Google Maps API error: {data['status']}")

def send_notification(phone, message):
    """
    Send SMS notification using Twilio.
    Placeholder: Implement with Twilio SDK.
    """
    # from twilio.rest import Client
    # client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
    # message = client.messages.create(
    #     body=message,
    #     from_=Config.TWILIO_PHONE_NUMBER,
    #     to=phone
    # )
    # return message.sid
    print(f"Sending SMS to {phone}: {message}")
    return "mock_sid"
