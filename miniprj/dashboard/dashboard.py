import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(
    page_title="Smart Classroom Monitoring",
    layout="wide",
    page_icon="📊"
)

# Styling
st.markdown("""
    <style>
    body { background-color: #222831; color: white; }
    .main { background-color: #222831; }
    .metric-box {
        background-color: #393E46;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
        color: white;
        margin-bottom: 20px;
        text-align: center;
    }
    .header-text { font-size: 38px; color: #00ADB5; font-weight: bold; }
    .sub-header-text { font-size: 18px; color: #EEEEEE; }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<p class='header-text'>📊 Smart Classroom Monitoring Dashboard</p>", unsafe_allow_html=True)
st.markdown("<p class='sub-header-text'>Developed by Manikanta – CSE-IoT (GCET)</p>", unsafe_allow_html=True)
st.markdown("---")

API_URL = "http://10.229.221.30:5000/latest"

refresh_interval = 10

def fetch_data():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        else:
            st.error("❌ Failed to fetch data from Flask API.")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"⚠️ API Error: {e}")
        return pd.DataFrame()

placeholder = st.empty()

while True:
    with placeholder.container():
        df = fetch_data()
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values(by='timestamp', ascending=False)

            st.markdown("## 📡 Live Sensor Readings")

            # KPIs
            k1, k2, k3 = st.columns(3)
            with k1:
                st.markdown(f"<div class='metric-box'>🌡️<br><b>Temperature</b><br>{df['temperature'].iloc[0]} °C</div>", unsafe_allow_html=True)
            with k2:
                st.markdown(f"<div class='metric-box'>💧<br><b>Humidity</b><br>{df['humidity'].iloc[0]} %</div>", unsafe_allow_html=True)
            with k3:
                st.markdown(f"<div class='metric-box'>🌫️<br><b>Air Quality</b><br>{df['air_quality'].iloc[0]}</div>", unsafe_allow_html=True)

            # Devices
            fan_status = "✅ ON" if df['fan'].iloc[0] == 1 else "❌ OFF"
            light_status = "✅ ON" if df['light'].iloc[0] == 1 else "❌ OFF"
            st.markdown(f"### ⚙️ Devices: 🌀 Fan: **{fan_status}** | 💡 Light: **{light_status}**")

            # Last command
            last_cmd = df['last_command'].iloc[0]
            if last_cmd:
                st.info(f"🎤 Last Command: {last_cmd}")

            # IR counter
            st.success(f"👀 IR Count: {df['ir_count'].iloc[0]}")

            # Trends
            st.markdown("### 📈 Sensor Trends")
            c1, c2 = st.columns(2)
            c1.line_chart(df[['timestamp', 'temperature']].set_index('timestamp'))
            c2.line_chart(df[['timestamp', 'humidity']].set_index('timestamp'))

            with st.expander("📋 Full Sensor Data"):
                st.dataframe(df, use_container_width=True)

        else:
            st.warning("⚠️ No sensor data available. Please send data from NodeMCU.")

    time.sleep(refresh_interval)

