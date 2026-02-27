# app.py

import streamlit as st
from map_generator import generate_map_html
from file_export import save_launch_data
from config import NUM_DROPZONES

st.set_page_config(layout="wide")
st.title("🚀 Rocket Launch Monitoring")

# -------------------------
# Launch Information
# -------------------------

st.header("🛰 Launch Information")

mission = st.text_input("Mission")
launch_site = st.text_input("Launch Site")
launch_country = st.text_input("Country")
launch_date = st.date_input("Launch Date")

col1, col2 = st.columns(2)
start_time = col1.text_input("Window Start (HHMM)")
end_time = col2.text_input("Window End (HHMM)")

# -------------------------
# Dropzones
# -------------------------

dropzones = {}

for i in range(1, NUM_DROPZONES + 1):
    st.subheader(f"Dropzone {i}")

    vertices_input = st.text_area(
        f"DZ{i} Vertices (one per line)",
        height=120,
        key=f"dz{i}_vertices"
    )

    debris_input = st.text_area(
        f"DZ{i} Debris Points (one per line)",
        height=80,
        key=f"dz{i}_debris"
    )

    dropzones[f"DZ{i}"] = {
        "vertices": [v.strip() for v in vertices_input.splitlines() if v.strip()],
        "debris": [d.strip() for d in debris_input.splitlines() if d.strip()]
    }

# -------------------------
# Buttons (Same As PyQt)
# -------------------------

col_btn1, col_btn2 = st.columns(2)

preview_clicked = col_btn1.button("Preview Map")
save_clicked = col_btn2.button("Save Form")

# -------------------------
# Button Logic
# -------------------------

if preview_clicked:
    html = generate_map_html(
        launch_site=launch_site,
        dropzones=dropzones
    )
    st.components.v1.html(html, height=700)

if save_clicked:
    success = save_launch_data(
        form_data={
            "mission": mission,
            "launch_site": launch_site,
            "launch_country": launch_country,
            "launch_date": launch_date,
            "start_time": start_time,
            "end_time": end_time
        },
        dropzones=dropzones
    )

    if success:
        st.success("Data saved successfully!")
    else:
        st.error("Failed to save data.")