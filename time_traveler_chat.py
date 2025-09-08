import streamlit as st
from streamlit_autorefresh import st_autorefresh
from datetime import datetime, timedelta

st.set_page_config(page_title="Time Traveler Chat", page_icon="⏳")

st.title("⏳ Time Traveler Chat")
st.write("Send a message that will be delivered at a future time (within a week).")

# Auto-refresh every 1 second
st_autorefresh(interval=1000, key="refresh")

# Initialize session state
if "scheduled" not in st.session_state:
    st.session_state.scheduled = []
if "delivered" not in st.session_state:
    st.session_state.delivered = []
if "date_str" not in st.session_state:
    st.session_state.date_str = datetime.now().strftime("%Y-%m-%d")
if "time_str" not in st.session_state:
    st.session_state.time_str = (datetime.now() + timedelta(minutes=1)).strftime("%H:%M")

# Inputs
msg_text = st.text_area("Message:", "")
st.session_state.date_str = st.text_input("Delivery Date (YYYY-MM-DD):", st.session_state.date_str)
st.session_state.time_str = st.text_input("Delivery Time (HH:MM, 24hr):", st.session_state.time_str)

# Schedule
if st.button("📩 Schedule Message"):
    try:
        delivery_dt = datetime.strptime(
            f"{st.session_state.date_str} {st.session_state.time_str}", "%Y-%m-%d %H:%M"
        )
        now = datetime.now()

        if now < delivery_dt <= now + timedelta(days=7):
            st.session_state.scheduled.append({"text": msg_text, "time": delivery_dt})
            st.success(f"✅ Message scheduled for {delivery_dt}")
        else:
            st.error("❌ Please pick a future time within 7 days.")
    except ValueError:
        st.error("❌ Invalid date or time format.")

# Check & deliver
now = datetime.now()
new_scheduled = []
for msg in st.session_state.scheduled:
    if now >= msg["time"]:
        if msg not in st.session_state.delivered:
            st.session_state.delivered.append(msg)
    else:
        new_scheduled.append(msg)
st.session_state.scheduled = new_scheduled

# Show delivered
st.subheader("📨 Delivered Messages:")
if st.session_state.delivered:
    for msg in st.session_state.delivered:
        st.write(f"**{msg['time'].strftime('%Y-%m-%d %H:%M')}** → {msg['text']}")
else:
    st.info("No messages delivered yet.")

