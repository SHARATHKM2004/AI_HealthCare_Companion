import streamlit as st
import requests
from geopy.distance import geodesic
import time

# OpenCage API Key
OPENCAGE_API_KEY = "9cd7deadfa1945a2b55cdaf00339e6ed"

# Function to get latitude and longitude from pincode
def get_coordinates_from_pincode(pincode):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={pincode}&key={OPENCAGE_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            location = data['results'][0]['geometry']
            return (location['lat'], location['lng'])
    return None

# Function to get nearby hospitals using Overpass API
def get_nearby_hospitals(lat, lon):
    query = f"""
    [out:json];
    (
      node["amenity"="hospital"](around:5000, {lat}, {lon});
    );
    out body;
    """
    response = requests.get("http://overpass-api.de/api/interpreter", params={'data': query})
    if response.status_code == 200:
        results = response.json().get('elements', [])
        return [{'Name': elem['tags'].get('name', 'Unnamed Hospital'), 'Location': {'lat': elem['lat'], 'lon': elem['lon']}} for elem in results]
    else:
        return []

# Function to calculate the nearest hospital
def find_nearest_hospital(user_location, hospitals):
    distances = [geodesic(user_location, (hospital['Location']['lat'], hospital['Location']['lon'])).km for hospital in hospitals]
    nearest_hospital = hospitals[distances.index(min(distances))]
    return nearest_hospital

# Streamlit UI
st.title("🚑 Health Emergency - Quick Ambulance Booking")
st.subheader("Book your ambulance here with ease, we’ll be there in no time to assist you!")

menu = st.sidebar.selectbox("Navigation", ["Home", "Book Ambulance", "Nearby Hospitals"])

if menu == "Book Ambulance":
    st.subheader("🚑 Ambulance Booking Service")

    # Step 1: Ask for Complete Address
    full_address = st.text_input("Enter Your Complete Address with Pincode")

    if full_address:
        # Extract pincode from address
        pincode = full_address.split()[-1]  # Assuming pincode is the last part of the address
        coordinates = get_coordinates_from_pincode(pincode)

        if coordinates:
            user_location = coordinates

            # Confirmation Message and Booking Process
            if st.button("Confirm Address and Book Ambulance"):
                with st.spinner("Finding the nearest hospital and ambulance for you..."):
                    time.sleep(2)  # Simulate booking delay

                    # Fetch nearby hospitals
                    hospitals = get_nearby_hospitals(user_location[0], user_location[1])

                    if hospitals:
                        # Find the nearest hospital
                        nearest_hospital = find_nearest_hospital(user_location, hospitals)

                        # Display booking details
                        st.success(f"Ambulance booked! 🚑\n\nWe’re on our way to your location: {full_address}!")
                        st.write(f"Nearest Hospital: {nearest_hospital['Name']} - Location: ({nearest_hospital['Location']['lat']}, {nearest_hospital['Location']['lon']})")
                    else:
                        st.error("No hospitals found nearby.")
        else:
            st.error("Invalid pincode. Please enter a valid one.")

elif menu == "Nearby Hospitals":
    st.subheader("Nearby Hospitals")

    # Step 1: Ask for Complete Address
    full_address = st.text_input("Enter Your Complete Address with Pincode")

    if full_address:
        # Extract pincode from address
        pincode = full_address.split()[-1]  # Assuming pincode is the last part of the address
        coordinates = get_coordinates_from_pincode(pincode)

        if coordinates:
            user_location = coordinates

            # Fetch nearby hospitals
            hospitals = get_nearby_hospitals(user_location[0], user_location[1])

            if hospitals:
                st.write("Nearby Hospitals:")
                for hospital in hospitals:
                    st.write(f"*Name:* {hospital['Name']} - *Location:* ({hospital['Location']['lat']}, {hospital['Location']['lon']})")
            else:
                st.write("No hospitals found nearby.")
        else:
            st.write("Invalid pincode. Please enter a valid one.")
