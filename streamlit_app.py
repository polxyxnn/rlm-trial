import streamlit as st
import pandas as pd
import io
from datetime import datetime
from streamlit_folium import st_folium

from map_generator import generate_map
from config import NUM_DROPZONES

# -----------------------------
# SESSION STATE INIT
# -----------------------------

if "dropzones" not in st.session_state:
    st.session_state.dropzones = {
        f"DZ{i}": {"vertices": [""], "debris": []}
        for i in range(1, NUM_DROPZONES + 1)
    }

if "map_obj" not in st.session_state:
    st.session_state.map_obj = None

# -----------------------------
# MAIN APP
# -----------------------------

st.set_page_config(layout="wide")

st.title("🚀 Rocket Launch Monitoring – Philippine Space Agency")
st.markdown("**Philippine Space Agency**")

# -----------------------------
# SIDEBAR FORM
# -----------------------------

with st.sidebar:

    st.header("Launch Information")

    mission = st.text_input("Mission Name", "")
    country = st.selectbox(
        "Launching Country",
        ["Select...", "China", "Japan", "North Korea", "South Korea", "Other"]
    )
    launch_site = st.text_input("Launch Site")
    launch_date = st.date_input("Launch Date", value=datetime.today())
    start_time = st.text_input("Window Start (HHMM)", "0745")
    end_time = st.text_input("Window End (HHMM)", "0810")

    st.header("Dropzones")

    for dz_id in st.session_state.dropzones:

        with st.expander(f"Dropzone {dz_id[2:]}", expanded=False):

            # ------------------ VERTICES ------------------
            vertices = st.session_state.dropzones[dz_id]["vertices"]

            if st.button("Add Vertex", key=f"add_v_{dz_id}"):
                vertices.append("")
                st.rerun()

            for i in range(len(vertices)):
                col1, col2 = st.columns([5, 1])

                vertices[i] = col1.text_input(
                    f"V{i+1}",
                    value=vertices[i],
                    key=f"v_{dz_id}_{i}"
                )

                if col2.button("×", key=f"del_v_{dz_id}_{i}"):
                    vertices.pop(i)
                    st.rerun()

            # ------------------ DEBRIS ------------------
            debris = st.session_state.dropzones[dz_id]["debris"]

            if st.button("Add Debris Point", key=f"add_d_{dz_id}"):
                debris.append("")
                st.rerun()

            for i in range(len(debris)):
                col1, col2 = st.columns([5, 1])

                debris[i] = col1.text_input(
                    f"D{i+1}",
                    value=debris[i],
                    key=f"d_{dz_id}_{i}"
                )

                if col2.button("×", key=f"del_d_{dz_id}_{i}"):
                    debris.pop(i)
                    st.rerun()

# -----------------------------
# MAIN CONTENT AREA
# -----------------------------

col_preview, col_map = st.columns([1, 4])

# -----------------------------
# PREVIEW MAP BUTTON
# -----------------------------

if col_preview.button("Preview Map", use_container_width=True):
    fmap = generate_map(
        launch_site,
        mission,
        country,
        launch_date,
        st.session_state.dropzones
    )
    st.session_state.map_obj = fmap
    st.rerun()

# -----------------------------
# DISPLAY MAP
# -----------------------------

if st.session_state.map_obj:
    st_folium(
        st.session_state.map_obj,
        width=1000,
        height=600,
        returned_objects=[]
    )

# -----------------------------
# EXPORT SECTION
# -----------------------------

st.subheader("Export Options")

col_save, col_export_map = st.columns(2)

# -----------------------------
# SAVE FORM (CSV + Excel)
# -----------------------------

if col_save.button("Save Form (CSV & Excel)", use_container_width=True):

    data = {
        "Mission": [mission],
        "Country": [country],
        "Site": [launch_site],
        "Date": [launch_date.strftime("%Y-%m-%d")],
    }

    df = pd.DataFrame(data)

    # CSV
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_bytes = csv_buffer.getvalue().encode()

    # Excel
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Launch Info")
    excel_bytes = excel_buffer.getvalue()

    st.download_button(
        label="Download CSV",
        data=csv_bytes,
        file_name=f"Info_{launch_date.strftime('%m%d%y')}.csv",
        mime="text/csv"
    )

    st.download_button(
        label="Download Excel",
        data=excel_bytes,
        file_name=f"Info_{launch_date.strftime('%m%d%y')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# -----------------------------
# EXPORT MAP
# -----------------------------

if col_export_map.button("Export Map (HTML)", use_container_width=True):

    if st.session_state.map_obj:

        html_buffer = io.StringIO()
        st.session_state.map_obj.save(html_buffer)
        html_bytes = html_buffer.getvalue().encode()

        st.download_button(
            label="Download Map HTML",
            data=html_bytes,
            file_name=f"Map_{datetime.now().strftime('%Y%m%d')}.html",
            mime="text/html"
        )

    else:
        st.warning("Preview the map first.")