# Natural Disaster Predictor

**DisasterSense** is a web-based application developed using Python, Streamlit, and machine learning to predict natural disasters in Japan. It offers real-time predictions for earthquakes and storms using geographic and meteorological inputs, supported by live weather integration and an interactive map-based interface. The tool is designed for educational and demonstration purposes, showcasing the potential of AI in disaster awareness and response.

## Earthquake Prediction
- **Input Parameters**:
  - Latitude & Longitude (selected via map or entered manually)

- **Prediction**:  
  A regression model trained on fault line and seismic data predicts:
  - Estimated number of days until the next potential earthquake
  - Estimated magnitude


<p align="center">
<img src="https://github.com/user-attachments/assets/7b963abb-455e-47a9-b9d2-b7e8e4cb3b5f" width="500">
</p>

- **Data Integration**:  
  Two datasets were combined:
  - Fault line coordinates (latitude and longitude)
  - Earthquake records in Japan since 2018 (latitude, longitude, magnitude)

  An earthquake was linked to a fault line if it occurred within a 10 km radius. For each fault, the model calculated the average earthquake magnitude and the average time interval (in days) between quakes for training.

<p align="center">
<img src="https://github.com/user-attachments/assets/35ede53e-24c2-4dbf-9cae-04c669afb236" width="500">
</p>
<p align="center">
<img src="https://github.com/user-attachments/assets/db2c4635-cdd1-4d88-9a00-b93773c426e3" width="500">
</p>
<p align="center">
<img src="https://github.com/user-attachments/assets/558dd04f-ba5a-4bd4-9fe8-0e3a4a014d33" width="500">
</p>
<p align="center">
<img src="https://github.com/user-attachments/assets/ad834f67-4a76-49e1-a0fd-9d3b3aca39db" width="500">
</p>

## Storm Prediction
- **Input Parameters**:
  - Latitude & Longitude (selected via interactive map or entered manually)
  - Temperature (fetched using **OpenWeatherMap API** or entered manually)
  - Humidity
  - Precipitation

- **Prediction**:  
  A **Random Forest Regression** model forecasts storm probability using the input parameters. Humidity is used to refine the prediction to reflect environmental effects.

<p align="center">
<img src="https://github.com/user-attachments/assets/5537b893-b628-40c6-8810-ea8456466791" width="500">
</p>

- **Data Integration**:  
  Two datasets were merged:
  - Storm events dataset (date, time, latitude, longitude)
  - City-level weather dataset (mean/max/min temperature, precipitation, humidity)

  Each storm was assigned to a city if it occurred within a 200 km radius on the same date. Storm count per city was used as a target variable alongside weather features.

<p align="center">
<img src="https://github.com/user-attachments/assets/44185680-3ce6-4a5c-8eb3-bfe5a906563b" width="500">
</p>
<p align="center">
<img src="https://github.com/user-attachments/assets/001cb75d-18e9-4d11-99f7-6ef37d3a24ca" width="500">
</p>
<p align="center">
<img src="https://github.com/user-attachments/assets/65336ac8-f635-45d8-8dc0-6e1ed1e4140d" width="500">
</p>

## Technologies Used
- **Python**: Core programming language
- **Streamlit**: Web application interface
- **scikit-learn**: Model development and training
- **pandas** & **numpy**: Data processing
- **joblib**: Model serialization
- **OpenWeatherMap API**: Real-time temperature data
- **Folium** and **Streamlit-Folium**: Interactive map for geographic input

## System Workflow
- The user selects prediction type: Earthquake or Storm
- The user clicks on the map or manually enters coordinates
- For Earthquake Prediction:
  - The model estimates the time and magnitude of a possible earthquake
- For Storm Prediction:
  - The user inputs humidity and precipitation
  - Temperature is either entered or fetched live
  - The model calculates and displays the storm probability

## Dataset and Model Training
- Models were trained on cleaned and merged datasets using **Random Forest Regression**
- Earthquake features: Fault location, average magnitude, and average days between events
- Storm features: Geographic coordinates, temperature, humidity, precipitation, and storm frequency
- Models were serialized using **joblib** for integration with Streamlit

## Results
- Earthquake predictions reflect fault line activity and location-based seismic trends
- Storm predictions vary based on weather inputs and proximity to storm-prone regions
- Real-time interactive results are presented through the user interface

## Disclaimer
This application is intended solely for educational and demonstrative purposes. It is not a replacement for official warnings or emergency planning tools.

## Data Sources
- Datasets were sourced from the **Japan Seismic Hazard Information Station (J-SHIS)**:  
  [https://www.j-shis.bosai.go.jp/en/downloads](https://www.j-shis.bosai.go.jp/en/downloads)
