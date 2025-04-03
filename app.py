import streamlit as st
from pymongo import MongoClient
import datetime

# MongoDB Connection
MONGO_URI = "mongodb+srv://raghavendrahande:L7HtjpVu3YTWXoHz@cluster0.rlrwisw.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client["goal_tracker"]
users_collection = db["users"]
goals_collection = db["goals"]

# User Login / Registration
def authenticate_user(username):
    user = users_collection.find_one({"username": username})
    if not user:
        users_collection.insert_one({"username": username, "streak": 0})
        return {"username": username, "streak": 0}
    return user

# Save Daily Goals
def save_goal(username, goal_text):
    today = datetime.date.today().isoformat()
    goals_collection.insert_one({"username": username, "date": today, "goal": goal_text, "completed": False})

# Mark Goal as Completed
def update_goal(username, goal_text, completed):
    today = datetime.date.today().isoformat()
    goals_collection.update_one({"username": username, "date": today, "goal": goal_text}, {"$set": {"completed": completed}})

# Calculate Streaks
def update_streak(username):
    streak = 0
    completed_days = sorted([
        entry["date"] for entry in goals_collection.find({"username": username, "completed": True})
    ])
    for i in range(len(completed_days) - 1, -1, -1):
        if i > 0 and (datetime.date.fromisoformat(completed_days[i]) - datetime.date.fromisoformat(completed_days[i - 1])).days == 1:
            streak += 1
        else:
            break
    users_collection.update_one({"username": username}, {"$set": {"streak": streak}})

# Streamlit UI
st.title("📆 Daily Goal Tracker")
st.write("Hello! If you see this, Streamlit is working.")

username = st.text_input("Enter your username to continue:")
if username:
    user = authenticate_user(username)
    st.write(f"Welcome, {user['username']}! Your current streak: 🔥 {user['streak']} days")

    st.subheader("✅ Set Your Goal for Today")
    goal_text = st.text_input("Enter your goal:")
    if st.button("Save Goal"):
        save_goal(username, goal_text)
        st.success("Goal saved!")

    st.subheader("🔄 End-of-Day Review")
    today_goals = list(goals_collection.find({"Username": username, "Date": datetime.date.today().isoformat()}))
    
    for goal in today_goals:
        completed = st.checkbox(goal["goal"], value=goal["completed"])
        update_goal(username, goal["goal"], completed)
    
    if st.button("Update Streak"):
        update_streak(username)
        st.success("Streak updated !")

