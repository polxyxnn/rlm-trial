# app.py

import streamlit as st
from map_generator import generate_map_html
from file_export import save_launch_data
from config import NUM_DROPZONES

st.set_page_config(layout="wide")
st.title("🚀 Rocket Launch Monitoring")

mission = st.text_input("Mission")
launch_site = st.text_input("Launch Site")
launch_date = st.date_input("Launch Date")

dropzones = {}

for i in range(1, NUM_DROPZONES + 1):
    st.subheader(f"Dropzone {i}")
    vertices = st.text_area(f"DZ{i} Vertices", key=f"dz{i}")
    dropzones[f"DZ{i}"] = {
        "vertices": vertices.splitlines(),
        "debris": []
    }

if st.button("Preview Map"):
    html = generate_map_html(launch_site, dropzones)
    st.components.v1.html(html, height=700)

if st.button("Save"):
    save_launch_data(
        {
            "mission": mission,
            "launch_site": launch_site,
            "launch_country": "",
            "launch_date": launch_date
        },
        dropzones
    )
    st.success("Saved successfully.")