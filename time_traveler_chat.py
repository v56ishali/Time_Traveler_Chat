import streamlit as st
from datetime import datetime
import json
import os

st.set_page_config(page_title="⏳ Time Traveler Chat", page_icon="⏳")

# 🔄 Auto-refresh every 1 second
st_autorefresh = st.experimental_autorefresh(interval=1000, key="refresh")

DATA_FILE = "messages.json"

# Load messages
def load_messages():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# Save messages
def save_messages(messages):
    with open(DATA_FILE, "w") as f:
        json.dump(messages, f)

# Deliver messages at exact time
def deliver_messages(messages):
    now = datetime.now()
    changed = False
    for msg in messages:
        delivery_time = datetime.fromisoformat(msg["time"])
        if not msg["delivered"] and now >= delivery_time:
            msg["delivered"] = True
            changed = True
    if changed:
        save_messages(messages)

# Load stored messages
messages = load_messages()

st.title("⏳ Time Traveler Chat")
st.write("Send a message that will be delivered at a future time (within a week).")

# Input
msg_text = st.text_area("Message:")
date_input = st.text_input("Delivery Date (YYYY-MM-DD):", value=datetime.now().strftime("%Y-%m-%d"))
time_input = st.text_input("Delivery Time (HH:MM in 24hr):", value=datetime.now().strftime("%H:%M"))

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

# Deliver automatically
deliver_messages(messages)

# Show delivered
st.subheader("📬 Delivered Messages:")
for msg in messages:
    if msg["delivered"]:
        st.write(f"✅ {datetime.fromisoformat(msg['time']).strftime('%Y-%m-%d %H:%M')} → {msg['text']}")
