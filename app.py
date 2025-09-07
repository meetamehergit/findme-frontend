# Frontend for the FindMe Marathon Photo Finder
# Hosted on Streamlit Cloud

import streamlit as st
import requests
import os
import time

# Load the backend URL from Streamlit's secrets
BACKEND_URL = os.getenv("BACKEND_URL")

st.set_page_config(
    page_title="FindMe: Your Marathon Photos",
    page_icon="🏃",
    layout="centered"
)

# --- UI Components ---
st.title("🏃 FindMe: Your Marathon Photos")
st.markdown("Upload a selfie or a race photo to automatically find all your pictures from the event.")

if not BACKEND_URL:
    st.error("Backend URL is not configured. Please set the 'BACKEND_URL' secret in Streamlit Cloud.")
else:
    # File uploader
    uploaded_file = st.file_uploader("Upload a photo...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        try:
            # Display spinner while processing
            with st.spinner("Searching for your photos... This might take a few moments."):
                files = {"runner_photo": uploaded_file.getvalue()}
                response = requests.post(f"{BACKEND_URL}/search", files=files, timeout=60)
            
            # Check the response status
            if response.status_code == 200:
                data = response.json()
                status = data.get("status")

                if status == "success":
                    matches = data.get("matches", [])
                    st.success(f"Found {len(matches)} matching photos!")
                    
                    st.markdown("Here are the links to your photos:")
                    
                    for link in matches:
                        st.markdown(f"[{link}]({link})")
                        
                elif status == "no_face_detected":
                    st.warning("Could not detect a face in your photo. Please try a different one with a clear view of your face.")
                elif status == "no_match_found":
                    st.info("No matching photos found in our database. Please try another photo or check back later.")
                elif status == "no_photos_indexed":
                    st.info("The marathon photos have not been indexed yet. Please check back later.")
            
            else:
                st.error(f"Error from the backend: {response.status_code} - {response.text}")
                st.error("Please contact the administrator or try again later.")
        
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to connect to the backend. Please check the backend URL or try again later. Error: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

st.markdown("---")
st.markdown("Powered by FastAPI, Hugging Face Spaces, and Streamlit Cloud.")
