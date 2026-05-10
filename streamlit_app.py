import streamlit as st
from PIL import Image

st.set_page_config(page_title="AI Attendance System")

st.title("IEEE Hybrid AI Attendance System")

st.subheader("Webcam Attendance Demo")

img = st.camera_input("Capture Student Face")

if img is not None:

    image = Image.open(img)

    st.image(image)

    st.success("Face Captured Successfully")