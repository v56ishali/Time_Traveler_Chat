import streamlit as st
from datetime import datetime

st.set_page_config(page_title="⏳ Time Traveler Chat", layout="centered")

st.title("⏳ Time Traveler Chat")
st.write("Send a message that will be delivered at a future time (within a week).")

# Session state setup
if "scheduled" not in st.session_state:
    st.session_state.scheduled = []
if "delivered" not in st.session_state:
    st.session_state.delivered = []

# User inputs
message = st.text_area("Message:")
date_input = st.text_input("Delivery Date (YYYY-MM-DD):")
time_input = st.text_input("Delivery Time (HH:MM, 24hr):")

# Schedule message
if st.button("📅 Schedule Message"):
    try:
        delivery_dt = datetime.strptime(f"{date_input} {time_input}", "%Y-%m-%d %H:%M")
        st.session_state.scheduled.append({"msg": message, "time": delivery_dt})
        st.success(f"✅ Message scheduled for {delivery_dt}")
    except Exception as e:
        st.error("⚠️ Invalid date or time format. Use YYYY-MM-DD and HH:MM (24hr).")

# Check and deliver messages
now = datetime.now().replace(second=0, microsecond=0)
new_schedule = []

for item in st.session_state.scheduled:
    delivery_time = item["time"].replace(second=0, microsecond=0)
    if now >= delivery_time:
        if item not in st.session_state.delivered:
            st.session_state.delivered.append(item)
    else:
        new_schedule.append(item)

st.session_state.scheduled = new_schedule

# Delivered messages
st.subheader("📨 Delivered Messages:")
if st.session_state.delivered:
    for d in st.session_state.delivered:
        st.info(f"🕒 {d['time']} → 💌 {d['msg']}")
else:
    st.warning("No messages delivered yet.")

# Auto-refresh every second
st.query_params(dummy=str(datetime.now()))

