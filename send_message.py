import streamlit as st
from twilio.rest import Client
from pymongo import MongoClient
import os

# Load credentials from Streamlit secrets
TWILIO_SID = st.secrets["TWILIO_SID"]
TWILIO_AUTH_TOKEN = st.secrets["TWILIO_AUTH_TOKEN"]
MONGO_URI = st.secrets["MONGO_URI"]
WHATSAPP_FROM = "whatsapp:+14155238886"  # Twilio Sandbox
WHATSAPP_TO = "whatsapp:+919110819421"  # Change to your number

# MongoDB Connection
client = MongoClient(MONGO_URI)
db = client["goal_tracker"]
users_collection = db["users"]

# Get Streaks
streak_data = list(users_collection.find({}, {"_id": 0, "username": 1, "streak": 1}))
message_body = "\n".join([f"🔥 {user['username']}: {user['streak']} days" for user in streak_data])

# Send WhatsApp Message
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
message = client.messages.create(
    from_=WHATSAPP_FROM,
    to=WHATSAPP_TO,
    body=f"📢 **Daily Streak Updates** 🔥\n{message_body}"
)

st.write("✅ WhatsApp message sent!")
