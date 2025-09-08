import streamlit as st
from datetime import datetime, date, time
from streamlit_autorefresh import st_autorefresh  # ✅ correct import

# Auto refresh every 1 sec
st_autorefresh(interval=1000, key="refresh")

st.title("⏳ Time Traveler Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "delivered" not in st.session_state:
    st.session_state.delivered = []

msg = st.text_input("Message:")
msg_date = st.date_input("Delivery Date (YYYY-MM-DD):", min_value=date.today())
msg_time = st.text_input("Delivery Time (HH:MM in 24hr):", value="12:00")

if st.button("✉️ Schedule Message"):
    try:
        h, m = map(int, msg_time.split(":"))
        deliver_at = datetime.combine(msg_date, time(h, m))
        st.session_state.messages.append({"msg": msg, "time": deliver_at})
        st.success(f"✅ Message scheduled for {deliver_at}")
    except:
        st.error("❌ Invalid time format. Use HH:MM in 24hr format.")

# Deliver messages
now = datetime.now()
remaining = []
for m in st.session_state.messages:
    if now >= m["time"]:
        st.session_state.delivered.append(m)
    else:
        remaining.append(m)
st.session_state.messages = remaining

st.subheader("📬 Delivered Messages:")
for d in st.session_state.delivered:
    st.write(f"{d['time']} → {d['msg']}")
