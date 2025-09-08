import streamlit as st
from streamlit_autorefresh import st_autorefresh
from datetime import datetime, timedelta

# Auto refresh every 1 second
st_autorefresh(interval=1000, key="refresh")

st.title("⏳ Time Traveler Chat")
st.write("Send a message that will be delivered at a future time (within a week).")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []  # stores scheduled messages
if "delivered" not in st.session_state:
    st.session_state.delivered = []  # stores delivered messages

# Input fields
msg_text = st.text_area("Message:")
date_str = st.text_input("Delivery Date (YYYY-MM-DD):", datetime.now().strftime("%Y-%m-%d"))
time_str = st.text_input("Delivery Time (HH:MM, 24hr):", datetime.now().strftime("%H:%M"))

if st.button("📩 Schedule Message"):
    try:
        delivery_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        now = datetime.now()

        if now < delivery_dt <= now + timedelta(days=7):
            st.session_state.messages.append({"text": msg_text, "time": delivery_dt})
            st.success(f"✅ Message scheduled for {delivery_dt}")
        else:
            st.error("❌ Please pick a future time within 7 days.")
    except ValueError:
        st.error("❌ Invalid date or time format.")

# Deliver messages automatically
now = datetime.now()
remaining_messages = []
for msg in st.session_state.messages:
    if now >= msg["time"]:
        if msg not in st.session_state.delivered:
            st.session_state.delivered.append(msg)
    else:
        remaining_messages.append(msg)
st.session_state.messages = remaining_messages

# Show delivered messages
st.subheader("📨 Delivered Messages:")
for msg in st.session_state.delivered:
    st.write(f"{msg['time']} → {msg['text']}")
