import os
from dotenv import load_dotenv
from twilio.rest import Client
from pymongo import MongoClient

# Load environment variables from .env file
load_dotenv()

# Fetch secrets from environment variables
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
WHATSAPP_FROM = os.getenv("WHATSAPP_FROM")
WHATSAPP_TO = os.getenv("WHATSAPP_TO")
MONGO_URI = os.getenv("MONGO_URI")

# Initialize Twilio client
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# Initialize MongoDB client
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["goal_tracker"]
users_collection = db["users"]

# Get Streaks
streak_data = list(users_collection.find({}, {"_id": 0, "username": 1, "streak": 1}))
message_body = "\n".join([f"🔥 {user['username']}: {user['streak']} days" for user in streak_data])

# Send Message
client.messages.create(
    from_=WHATSAPP_FROM,
    to=WHATSAPP_TO,
    body=f"📢 **Daily Streak Updates** 🔥\n{message_body}"
)

print("WhatsApp message sent!")
