import streamlit as st
import numpy as np
import joblib
import os
import pandas as pd
import requests
from streamlit_folium import st_folium
import folium

OPENWEATHER_API_KEY = ""
data_dir = "data"
storm_model_path = os.path.join(data_dir, "model.pkl")
earthquake_model_path = os.path.join(data_dir, "model2.pkl")

storm_model = joblib.load(storm_model_path)
earthquake_model = joblib.load(earthquake_model_path)

def fetch_live_weather(lat, lon):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        temp = data["main"]["temp"]
        return temp
    except Exception as e:
        st.warning(f"⚠️ Could not fetch live temperature data: {e}")
        return None

def create_japan_map():
    japan_bounds = [[24.396308, 122.93457], [45.551483, 153.986672]]
    m = folium.Map(
        location=[36.2048, 138.2529],
        zoom_start=5,
        min_zoom=4,
        max_zoom=8,
        max_bounds=True,
    )
    m.fit_bounds(japan_bounds)
    m.add_child(folium.LatLngPopup())
    return m

st.set_page_config(page_title="Disaster Predictor", page_icon="🌍")
st.title("🌪️🌍 DisasterSense")

prediction_type = st.selectbox("What do you want to predict?", ["Select...", "Storm", "Earthquake"])

if prediction_type in ["Storm", "Earthquake"]:
    st.markdown("### 🗾 Click on the map or enter coordinates manually")

    # Initialize session state for lat/lon and live temp
    if "clicked_lat" not in st.session_state:
        st.session_state.clicked_lat = 35.0
    if "clicked_lon" not in st.session_state:
        st.session_state.clicked_lon = 137.0
    if "live_temp" not in st.session_state:
        st.session_state.live_temp = 20.0

    map_col, input_col = st.columns([2, 1])

    with map_col:
        m = create_japan_map()
        map_data = st_folium(m, width=500, height=400)

        if map_data and map_data["last_clicked"]:
            st.session_state.clicked_lat = np.clip(map_data["last_clicked"]["lat"], -90.0, 90.0)
            st.session_state.clicked_lon = np.clip(map_data["last_clicked"]["lng"], -180.0, 180.0)

    with input_col:
        lat = st.number_input("Latitude", -90.0, 90.0, format="%.4f", value=st.session_state.clicked_lat, key="lat_input")
        lon = st.number_input("Longitude", -180.0, 180.0, format="%.4f", value=st.session_state.clicked_lon, key="lon_input")

        st.session_state.clicked_lat = lat
        st.session_state.clicked_lon = lon

        if prediction_type == "Storm":
            st.subheader("Storm Inputs")

            if st.button("Fetch Live Temperature"):
                temp = fetch_live_weather(lat, lon)
                if temp is not None:
                    st.session_state.live_temp = temp

            temp = st.number_input("Temperature (°C)", format="%.2f", value=st.session_state.live_temp)
            humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, step=0.1, format="%.2f")
            precip = st.number_input("Precipitation (mm)", format="%.2f")

            if st.button("Predict Storm"):
                input_data = np.array([[lat, lon, temp, precip]])
                pred = storm_model.predict(input_data)[0]

                humidity_factor = 0.5
                humidity_effect = humidity_factor * (humidity / 100) * (100 - pred)
                adjusted_pred = pred + humidity_effect
                adjusted_pred = np.clip(adjusted_pred, 0, 100)

                st.success(f"🌧️ **Storm Probability**: {adjusted_pred:.2f}%")

        elif prediction_type == "Earthquake":
            st.subheader("Earthquake Prediction")
            if st.button("Predict Earthquake"):
                input_df = pd.DataFrame([[lat, lon]], columns=["fault_latitude", "fault_longitude"])
                days, magnitude = earthquake_model.predict(input_df)[0]
                st.success(f"🌍 **Estimated Days Until Earthquake**: {int(round(days))} days")
                st.success(f"🌍 **Estimated Earthquake Magnitude**: {magnitude:.2f}")

else:
    st.info("👆 Please select a prediction type to begin.")
