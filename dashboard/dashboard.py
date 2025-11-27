import streamlit as st
import pandas as pd
import requests
import time

# ================== PAGE CONFIG ==================
st.set_page_config(
	page_title="🧠 Intelligent Classroom Dashboard",
	layout="wide",
	page_icon="📡"
)

# ================== CUSTOM CSS ==================
st.markdown("""
	<style>
	body { background-color: #222831; color: white; }
	.main { background-color: #222831; }
	.metric-box {
		background-color: #393E46;
		padding: 18px;
		border-radius: 15px;
		box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
		color: white;
		text-align: center;
		margin-bottom: 15px;
	}
	.header-text { font-size: 38px; color: #00ADB5; font-weight: bold; text-align: center; }
	.sub-header-text { font-size: 18px; color: #EEEEEE; text-align: center; margin-bottom: 20px; }
	</style>
""", unsafe_allow_html=True)

# ================== HEADER ==================
st.markdown("<p class='header-text'>📊 Intelligent Classroom Monitoring & Management Dashboard</p>", unsafe_allow_html=True)
st.markdown("<p class='sub-header-text'>Developed by Manikanta CSE (IoT) | Geethanjali College of Engineering & Technology</p>", unsafe_allow_html=True)
st.markdown("---")

# ================== API URL ==================
API_URL = "https://intelligent-classroom-management-and.onrender.com/latest"

REFRESH_INTERVAL = 10  # seconds

# ================== FETCH DATA ==================
# ================== FETCH DATA ==================
def fetch_data():
	try:
		response = requests.get(API_URL)
		if response.status_code == 200:
			data = response.json()
			if data:  # Check if data is not empty
				df = pd.DataFrame(data)
				if 'timestamp' in df.columns:
					df['timestamp'] = pd.to_datetime(df['timestamp'])
				else:
					df['timestamp'] = pd.to_datetime([])  # empty column to avoid errors
				return df
			else:
				return pd.DataFrame()
		else:
			st.error("❌ Failed to fetch data from Flask API.")
			return pd.DataFrame()
	except Exception as e:
		st.error(f"⚠️ API Error: {e}")
		return pd.DataFrame()


# ================== LIVE DASHBOARD ==================
placeholder = st.empty()

while True:
	with placeholder.container():
		df = fetch_data()
		if not df.empty:
			df['timestamp'] = pd.to_datetime(df['timestamp'])
			df = df.sort_values(by='timestamp', ascending=False)

			latest = df.iloc[0]

			# ========== TOP KPIs ==========
			st.markdown("## 🌡️ Real-Time Sensor Data")

			k1, k2, k3, k4 = st.columns(4)
			with k1:
				st.markdown(f"<div class='metric-box'>🌡️<br><b>Temperature</b><br>{latest['temperature']} °C</div>", unsafe_allow_html=True)
			with k2:
				st.markdown(f"<div class='metric-box'>💧<br><b>Humidity</b><br>{latest['humidity']} %</div>", unsafe_allow_html=True)
			with k3:
				st.markdown(f"<div class='metric-box'>🌫️<br><b>Air Quality (MQ135)</b><br>{latest['air_quality']}</div>", unsafe_allow_html=True)
			with k4:
				st.markdown(f"<div class='metric-box'>💡<br><b>Light Level (LDR)</b><br>{latest['light_level']}</div>", unsafe_allow_html=True)

			c1, c2, c3 = st.columns(3)
			with c1:
				st.markdown(f"<div class='metric-box'>🎤<br><b>Sound Level</b><br>{latest['sound_level']}</div>", unsafe_allow_html=True)
			with c2:
				st.markdown(f"<div class='metric-box'>👁️<br><b>PIR Motion</b><br>{'Detected' if latest['pir_sensor'] else 'No Motion'}</div>", unsafe_allow_html=True)
			with c3:
				st.markdown(f"<div class='metric-box'>📡<br><b>IR Count</b><br>{latest['ir_count']}</div>", unsafe_allow_html=True)

			# ========== DEVICE STATUS ==========
			st.markdown("---")
			fan_status = "🌀 ON" if latest['fan_status'] == 1 else "🌀 OFF"
			light_status = "💡 ON" if latest['light_status'] == 1 else "💡 OFF"
			reason = latest['reason'] if 'reason' in df.columns else "No reason recorded."

			st.markdown(f"### ⚙️ Device Status")
			st.success(f"🌀 **Fan:** {fan_status}")
			st.success(f"💡 **Light:** {light_status}")
			st.info(f"🧠 **Reason:** {reason}")

			# ========== COMMAND INFO ==========
			if latest['last_command']:
				st.warning(f"🎤 Last Voice Command: `{latest['last_command']}`")

			# ========== SENSOR TREND CHARTS ==========
			st.markdown("---")
			st.markdown("## 📈 Sensor Trends (Last 10 Entries)")
			t1, t2 = st.columns(2)

			with t1:
				st.line_chart(df[['timestamp', 'temperature']].set_index('timestamp'), height=250)
				st.line_chart(df[['timestamp', 'air_quality']].set_index('timestamp'), height=250)
			with t2:
				st.line_chart(df[['timestamp', 'humidity']].set_index('timestamp'), height=250)
				st.line_chart(df[['timestamp', 'light_level']].set_index('timestamp'), height=250)

			# ========== ADDITIONAL CHARTS ==========
			st.markdown("## 🔊 Sound & Motion Activity")
			st.bar_chart(df[['timestamp', 'sound_level']].set_index('timestamp'), height=200)
			st.line_chart(df[['timestamp', 'ir_count']].set_index('timestamp'), height=200)

			# ========== FULL TABLE ==========
			with st.expander("📋 Full Sensor Log Data"):
				st.dataframe(df, use_container_width=True, height=400)

		else:
			st.warning("⚠️ No sensor data available. Please send data from NodeMCU.")
	time.sleep(REFRESH_INTERVAL)
