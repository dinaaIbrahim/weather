
import streamlit as st
import requests
import re

# --- Location via IP ---
def get_location():
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        loc = data.get("loc", "")
        latitude, longitude = loc.split(",") if loc else (None, None)
        return {
            "city": data.get("city", ""),
            "country": data.get("country", ""),
            "latitude": latitude,
            "longitude": longitude
        }
    except Exception as e:
        st.error(f"Error getting location: {e}")
        return None

def format_weather_details(current):
    return (
        f"Temperature: {current['temp_c']}°C / {current['temp_f']}°F\n"
        f"Humidity: {current['humidity']}%\n"
        f"Cloud Cover: {current['cloud']}%\n"
        f"Wind: {current['wind_kph']} kph ({current['wind_dir']})\n"
        f"Last Updated: {current['last_updated']}\n"
    )

# --- Weather Fetcher ---
def get_weather(location):
    weather_API_KEY = "c5a07223b4c645bdbc482155252805"
    if isinstance(location, str):
        query = location
    elif isinstance(location, tuple) and len(location) == 2:
        query = f"{location[0]},{location[1]}"
    else:
        st.error("Invalid location format.")
        return None

    url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": weather_API_KEY,
        "q": query,
        "aqi": "no"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch weather data: {response.status_code}")
        return None
    

def strict_country_validation(output: str) -> str:
    
    clean_output = re.split(r'[\n\(\)\-]', output)[0].strip()
    
    if clean_output.lower() == "none":
        return "None"
    
    if (clean_output.istitle() and 
        len(clean_output.split()) <= 3 and
        clean_output.isalpha() or ' ' in clean_output.replace('-', '')):
        return clean_output
    return "None"
