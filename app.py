import streamlit as st
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components

st.set_page_config(page_title="Farm Connect", layout="centered")

st.title("🌾 Farm Connect: Market & Security")

st.markdown("---")

# 📈 Market and Price Updates
st.header("📈 Market and Price Updates")
st.subheader("📊 Submit Crop Prices")
with st.form("submit_price"):
    crop = st.text_input("Crop Name")
    price = st.number_input("Price per unit (e.g. per kg)", min_value=0.0, step=0.1)
    location = st.text_input("Location")
    submitted = st.form_submit_button("Submit Price")
    if submitted and crop and location:
        if "market_data" not in st.session_state:
            st.session_state.market_data = []
        st.session_state.market_data.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "crop": crop,
            "price": price,
            "location": location
        })
        st.success("Price submitted successfully!")

if "market_data" in st.session_state and st.session_state.market_data:
    st.subheader("📈 Community Market Prices")
    df = pd.DataFrame(st.session_state.market_data)
    st.dataframe(df)

st.markdown("---")

# 🛡️ Security & Theft Alerts
st.header("🛡️ Security & Theft Alerts")
st.subheader("📍 Report with Location")

st.markdown("Click the button below to report an incident using your phone's location.")

components.html("""
    <button onclick="getLocation()" style="font-size:18px;padding:10px;margin:10px;">📍 Report Incident with Location</button>
    <script>
        function getLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function(position) {
                    const lat = position.coords.latitude;
                    const lon = position.coords.longitude;
                    const event = new CustomEvent("fromWebView", {
                        detail: { lat, lon }
                    });
                    window.dispatchEvent(event);
                });
            } else {
                alert("Geolocation is not supported by this browser.");
            }
        }
    </script>
""", height=100)

incident = st.text_area("Describe the issue (e.g. theft, suspicious activity)")

lat = st.experimental_get_query_params().get("lat", [None])[0]
lon = st.experimental_get_query_params().get("lon", [None])[0]

if st.button("📤 Submit Incident Report"):
    if incident:
        if "security_alerts" not in st.session_state:
            st.session_state.security_alerts = []
        st.session_state.security_alerts.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "incident": incident,
            "location": f"Lat: {lat}, Lon: {lon}" if lat and lon else "Unknown"
        })
        st.success("Incident reported with location!" if lat and lon else "Incident reported without location.")

if "security_alerts" in st.session_state and st.session_state.security_alerts:
    st.subheader("📋 Recent Alerts")
    alerts_df = pd.DataFrame(st.session_state.security_alerts)
    st.dataframe(alerts_df)
