# config.py

from pathlib import Path

# Base directory of project
BASE_DIR = Path(__file__).resolve().parent

# Assets directory
ASSETS_DIR = BASE_DIR / "assets"
SHAPEFILES_DIR = ASSETS_DIR / "shapefiles"
LOGO_DIR = ASSETS_DIR / "logos"
OUTPUT_DIR = BASE_DIR / "outputs"

# Ensure output directory exists
OUTPUT_DIR.mkdir(exist_ok=True)

# Data files
LAUNCH_SITE_CSV = SHAPEFILES_DIR / "Launch_Centers_Coords.csv"
MANILA_FIR_SHP = SHAPEFILES_DIR / "Manila_FIR_boundary.shp"
BASELINE_SHP = SHAPEFILES_DIR / "PH_Baseline.shp"
KEY_LOCATIONS_SHP = SHAPEFILES_DIR / "Updated_Key_Locations.shp"
EEZ_SHP = SHAPEFILES_DIR / "eez.shp"

# Logo
PHILSA_LOGO = LOGO_DIR / "PhilSA_v1-01.png"

# Constants
NUM_DROPZONES = 4
MAX_VERTICES = 8
MAX_DEBRIS = 4
PH_TIME_OFFSET = 8  # UTC +8