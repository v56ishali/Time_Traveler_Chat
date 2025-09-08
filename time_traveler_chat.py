import streamlit as st
from datetime import datetime
import time
import json
import os

st.set_page_config(page_title="⏳ Time Traveler Chat", page_icon="⏳")

# File to save scheduled messages
DATA_FILE = "messages.json"

# Load messages from file
def load_messages():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# Save messages to file
def save_messages(messages):
    with open(DATA_FILE, "w") as f:
        json.dump(messages, f)

# Deliver due messages
def deliver_messages(messages):
    now = datetime.now()
    delivered = []
    for msg in messages:
        delivery_time = datetime.fromisoformat(msg["time"])
        if not msg["delivered"] and now >= delivery_time:
            msg["delivered"] = True
            delivered.append(f"{now.strftime('%Y-%m-%d %H:%M:%S')} → {msg['text']}")
    save_messages(messages)
    return delivered

# Load stored messages
messages = load_messages()

st.title("⏳ Time Traveler Chat")
st.write("Send a message that will be delivered at a future time (within a week).")

# Input for new message
msg_text = st.text_area("Message:")
date_input = st.text_input("Delivery Date (YYYY-MM-DD):", value=datetime.now().strftime("%Y-%m-%d"))
time_input = st.text_input("Delivery Time (HH:MM in 24hr):", value=(datetime.now().strftime("%H:%M")))

if st.button("📩 Schedule Message"):
    try:
        delivery_str = f"{date_input} {time_input}:00"
        delivery_time = datetime.fromisoformat(delivery_str)
        if delivery_time <= datetime.now():
            st.error("❌ Delivery time must be in the future!")
        elif (delivery_time - datetime.now()).days > 7:
            st.error("❌ Delivery must be within 7 days!")
        else:
            messages.append({"text": msg_text, "time": delivery_time.isoformat(), "delivered": False})
            save_messages(messages)
            st.success(f"✅ Message scheduled for {delivery_time}")
    except Exception as e:
        st.error(f"Invalid date/time format: {e}")

# Deliver messages automatically
delivered_now = deliver_messages(messages)

# Show delivered messages
st.subheader("📬 Delivered Messages:")
for msg in messages:
    if msg["delivered"]:
        st.write(f"✅ {datetime.fromisoformat(msg['time']).strftime('%Y-%m-%d %H:%M')} → {msg['text']}")
