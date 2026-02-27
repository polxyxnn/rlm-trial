# file_export.py

import pandas as pd
from config import OUTPUT_DIR


def save_launch_data(form_data, dropzones):
    date_str = form_data["launch_date"].strftime("%m%d%y")

    info_csv = OUTPUT_DIR / f"Info_{date_str}.csv"

    row = {
        "ROCKET NAME": form_data["mission"],
        "LAUNCHING STATE": form_data["launch_country"],
        "LAUNCH CENTER": form_data["launch_site"],
    }

    pd.DataFrame([row]).to_csv(info_csv, index=False)

    return True