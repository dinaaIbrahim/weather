import streamlit as st
import os
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"

st.set_page_config(page_title="Weather-Activity Assistant", layout="wide")  

import logging
logging.getLogger('streamlit.runtime.scriptrunner').setLevel(logging.ERROR)

from app.utils import get_location, format_weather_details, get_weather
from app.core import detect_country_llm, regenerate_query, generate_final_response

# Initialize session state
if 'weather_data' not in st.session_state:
    st.session_state.weather_data = None
if 'rewritten_query' not in st.session_state:
    st.session_state.rewritten_query = None
if 'final_response' not in st.session_state:
    st.session_state.final_response = None


# --- Streamlit UI ---
st.title("🌦️ Weather-Activity Assistant")
st.markdown("Want tips on what to do or wear in your location? Just ask — or say what you need, and we’ll figure out your location automatically!")

query = st.text_input("Enter your query:", placeholder="e.g., What should I wear in Paris today?")

if st.button("Submit"):
    if query:
        with st.spinner("Processing your request..."):
            # Step 1: Detect country 
            country_from_query = detect_country_llm(query).strip()
            
     
            weather_location = None
            location_source = ""
            effective_country = None
            city_name = None
            
            if country_from_query.lower() != "none":
             
                weather_location = country_from_query
                location_source = f"from your query: {country_from_query}"
                effective_country = country_from_query
            else:
                # Case 2: Fall back to IP detection - use lat/long
                ip_location = get_location()
                if ip_location:
                    
                    weather_location = (ip_location['latitude'], ip_location['longitude'])
                    location_source = (f"from your approximate location: {ip_location['city']}, "
                                     f"{ip_location['country']} ")
                    effective_country = ip_location['country']
                    city_name = ip_location['city']
                else:
                    st.error("Could not determine your location. Please include a country or city in your query.")
                    st.stop()

            # Step 2: Get weather data
            st.session_state.weather = get_weather(weather_location)
            
            if st.session_state.weather:
                current = st.session_state.weather['current']
                st.session_state.weather_details = format_weather_details(current)
             
                st.success(f"Location: {location_source}")
                
                # Step 3: Prepare for query regeneration
                location_for_query = ""
                if country_from_query.lower() != "none":
                    location_for_query = f"Country: {country_from_query}"
                elif city_name and effective_country:
                    location_for_query = f"Location: {city_name}, {effective_country}"
                
                # Step 4: Regenerate query
                st.session_state.rewritten_query = regenerate_query(
                    query, 
                    st.session_state.weather_details,
                    location_for_query  
                )
                
                # Step 5: Generate final response
                st.session_state.final_response = generate_final_response(st.session_state.rewritten_query)
            else:
                st.error("Could not retrieve weather data for the specified location.")
# Display results
if st.session_state.get('weather'):
    st.subheader("🌤️ Weather Details")
    st.text(st.session_state.weather_details)

if st.session_state.get('final_response'):
    st.subheader("💡 Recommendations")
    st.markdown(st.session_state.final_response)