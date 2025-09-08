import streamlit as st
from streamlit_autorefresh import st_autorefresh
from datetime import datetime, timedelta

# Auto refresh every 1 second
st_autorefresh(interval=1000, key="refresh")

st.title("⏳ Time Traveler Chat")
st.write("Send a message that will be delivered at a future time (within a week).")

# Initialize session state
if "scheduled" not in st.session_state:
    st.session_state.scheduled = []  # stores scheduled messages
if "delivered" not in st.session_state:
    st.session_state.delivered = []  # stores delivered messages

# Input fields
msg_text = st.text_area("Message:")
date_str = st.text_input("Delivery Date (YYYY-MM-DD):", datetime.now().strftime("%Y-%m-%d"))
time_str = st.text_input("Delivery Time (HH:MM, 24hr):", (datetime.now() + timedelta(minutes=1)).strftime("%H:%M"))

# Schedule new message
if st.button("📩 Schedule Message"):
    try:
        delivery_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        now = datetime.now()

        if now < delivery_dt <= now + timedelta(days=7):
            st.session_state.scheduled.append({"text": msg_text, "time": delivery_dt})
            st.success(f"✅ Message scheduled for {delivery_dt}")
        else:
            st.error("❌ Please pick a future time within 7 days.")
    except ValueError:
        st.error("❌ Invalid date or time format.")

# Deliver scheduled messages
now = datetime.now()
new_scheduled = []
for msg in st.session_state.scheduled:
    if now >= msg["time"]:
        if msg not in st.session_state.delivered:  # deliver only once
            st.session_state.delivered.append(msg)
    else:
        new_scheduled.append(msg)  # keep for future
st.session_state.scheduled = new_scheduled

# Show delivered messages
st.subheader("📨 Delivered Messages:")
if st.session_state.delivered:
    for msg in st.session_state.delivered:
        st.write(f"**{msg['time'].strftime('%Y-%m-%d %H:%M')}** → {msg['text']}")
else:
    st.info("No messages delivered yet.")
