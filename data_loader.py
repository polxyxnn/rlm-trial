# data_loader.py

import pandas as pd
import geopandas as gpd
from config import (
    LAUNCH_SITE_CSV,
    KEY_LOCATIONS_SHP,
)


def load_launch_sites():
    df = pd.read_csv(LAUNCH_SITE_CSV)

    return {
        str(row["Place"]).strip(): (float(row["Lat"]), float(row["Lon"]))
        for _, row in df.iterrows()
    }


def load_key_locations():
    key_locations = {}

    try:
        gdf = gpd.read_file(KEY_LOCATIONS_SHP)

        for _, row in gdf.iterrows():
            geom = row.geometry
            if geom and geom.geom_type == "Point":
                key_locations[str(row[0])] = (geom.y, geom.x)

    except Exception as e:
        print("Error loading key locations:", e)

    return key_locations