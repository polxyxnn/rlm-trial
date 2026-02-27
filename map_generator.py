# map_generator.py

import folium
from shapely.geometry import Polygon
import math
from coordinate_utils import parse_coordinates
from data_loader import load_launch_sites, load_key_locations


def generate_map_html(
    launch_site,
    dropzones
):
    launch_sites = load_launch_sites()
    key_locations = load_key_locations()

    polygons = []

    for dz_id, dz in dropzones.items():
        pts = []
        for coord in dz["vertices"]:
            lat, lon = parse_coordinates(coord)
            if lat and lon:
                pts.append((lat, lon))

        if len(pts) >= 3:
            polygons.append((dz_id, pts))

    if not polygons:
        return "<p>No valid coordinates</p>"

    all_coords = [p for _, pts in polygons for p in pts]
    avg_lat = sum(p[0] for p in all_coords) / len(all_coords)
    avg_lon = sum(p[1] for p in all_coords) / len(all_coords)

    fmap = folium.Map(location=[avg_lat, avg_lon], zoom_start=6)

    # Launch site marker
    if launch_site in launch_sites:
        lat, lon = launch_sites[launch_site]
        folium.Marker([lat, lon], popup="Launch Site").add_to(fmap)

    # Dropzone polygons
    for dzid, pts in polygons:
        folium.Polygon(
            locations=pts,
            color="green",
            fill=True,
            fill_opacity=0.3
        ).add_to(fmap)

    return fmap._repr_html_()