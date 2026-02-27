# coordinate_utils.py

import re
import math
from datetime import datetime, timedelta


def to_DM(lat, lon):
    def conv(d, is_lat=True):
        hemi = None
        if is_lat:
            hemi = 'N' if d >= 0 else 'S'
        else:
            hemi = 'E' if d >= 0 else 'W'
        d = abs(d)
        deg = int(d)
        minutes = (d - deg) * 60
        return f"{deg}°{minutes:.3f}'{hemi}"
    return f"{conv(lat, True)}, {conv(lon, False)}"

def parse_coordinates(coord_str):
    if not coord_str or not isinstance(coord_str, str):
        return None, None
    s = coord_str.strip().upper().replace(",", " ")
    # 1) DDMMSSN DDDMMSS[E/W]
    m = re.search(r'(\d{6})(?:\.\d+)?\s*([NS])\s+(\d{7})(?:\.\d+)?\s*([EW])', s)
    if m:
        lat_raw, lat_h, lon_raw, lon_h = m.groups()
        lat_deg = int(lat_raw[:2])
        lat_min = int(lat_raw[2:4])
        lat_sec = int(lat_raw[4:6])
        lon_deg = int(lon_raw[:3])
        lon_min = int(lon_raw[3:5])
        lon_sec = int(lon_raw[5:7])
        lat = lat_deg + lat_min / 60 + lat_sec / 3600
        lon = lon_deg + lon_min / 60 + lon_sec / 3600
        if lat_h == 'S':
            lat = -lat
        if lon_h == 'W':
            lon = -lon
        return round(lat, 6), round(lon, 6)
    # 2) Compact DM: NDDMM EDDDMM
    m = re.match(r'^([NS])(\d{2})(\d{2})\s*([EW])(\d{3})(\d{2})$', s.replace(" ", ""))
    if m:
        lat_h, lat_d, lat_m, lon_h, lon_d, lon_m = m.groups()
        lat = int(lat_d) + int(lat_m) / 60
        lon = int(lon_d) + int(lon_m) / 60
        if lat_h == 'S':
            lat = -lat
        if lon_h == 'W':
            lon = -lon
        return round(lat, 6), round(lon, 6)
    # 3) DMS with symbols or spaces
    dms = re.findall(r'(\d+)[°\s]+(\d+)[\'\s]+(\d+)[\"\s]*([NS])', s)
    dms_lon = re.findall(r'(\d+)[°\s]+(\d+)[\'\s]+(\d+)[\"\s]*([EW])', s)
    if dms and dms_lon:
        lat_d, lat_m, lat_s, lat_h = dms[0]
        lon_d, lon_m, lon_s, lon_h = dms_lon[0]
        lat = int(lat_d) + int(lat_m)/60 + int(lat_s)/3600
        lon = int(lon_d) + int(lon_m)/60 + int(lon_s)/3600
        if lat_h == 'S':
            lat = -lat
        if lon_h == 'W':
            lon = -lon
        return round(lat, 6), round(lon, 6)
    # 4) Decimal degrees with hemisphere
    lat_match = re.search(r'([-+]?\d+(?:\.\d+)?)\s*([NS])', s)
    lon_match = re.search(r'([-+]?\d+(?:\.\d+)?)\s*([EW])', s)
    if lat_match and lon_match:
        lat = float(lat_match.group(1))
        lon = float(lon_match.group(1))
        if lat_match.group(2) == 'S':
            lat = -abs(lat)
        if lon_match.group(2) == 'W':
            lon = -abs(lon)
        return round(lat, 6), round(lon, 6)
    # 5) Plain decimal "lat, lon"
    m = re.match(r'\s*([-+]?\d+(?:\.\d+)?)\s*[, \s]\s*([-+]?\d+(?:\.\d+)?)', s)
    if m:
        return round(float(m.group(1)), 6), round(float(m.group(2)), 6)
    return None, None

def convert_to_compact(raw_str):
    if not raw_str or str(raw_str).strip() == "":
        return ""
    s = str(raw_str).upper().replace(" ", "").strip()
    m = re.match(r'^([NS])(\d{2})(\d{2})([EW])(\d{3})(\d{2})$', s)
    if m:
        return f"{m.group(1)}{m.group(2)}{m.group(3)}{m.group(4)}{m.group(5)}{m.group(6)}"
    m2 = re.search(r'([NS])\s*(\d{2})(\d{2})\s*([EW])\s*(\d{3})(\d{2})', s)
    if m2:
        return f"{m2.group(1)}{m2.group(2)}{m2.group(3)}{m2.group(4)}{m2.group(5)}{m2.group(6)}"
    latlon = parse_coordinates(raw_str)
    if not latlon or latlon[0] is None or latlon[1] is None:
        return ""
    lat_dd, lon_dd = latlon
    def dd_to_compact(dd, is_lat=True):
        if is_lat:
            hemi = 'N' if dd >= 0 else 'S'
        else:
            hemi = 'E' if dd >= 0 else 'W'
        d = abs(dd)
        deg = int(d)
        minutes_full = (d - deg) * 60
        minute = int(minutes_full)
        sec = (minutes_full - minute) * 60
        if sec >= 30:
            minute += 1
            if minute == 60:
                minute = 0
                deg += 1
        if is_lat:
            return f"{hemi}{deg:02d}{minute:02d}"
        else:
            return f"{hemi}{deg:03d}{minute:02d}"
    return dd_to_compact(lat_dd, True) + dd_to_compact(lon_dd, False)

def utc_window_to_phst(window_utc: str) -> str:
    try:
        s = window_utc.upper().replace("UTC", "").strip()
        start_str, end_str = [x.strip() for x in s.split("-")]
        start_utc = datetime.strptime(start_str, "%H%M")
        end_utc = datetime.strptime(end_str, "%H%M")
        if end_utc <= start_utc:
            end_utc += timedelta(days=1)
        start_ph = start_utc + timedelta(hours=8)
        end_ph = end_utc + timedelta(hours=8)
        start_fmt = start_ph.strftime("%I:%M %p").lstrip("0")
        end_fmt = end_ph.strftime("%I:%M %p").lstrip("0")
        return f"{start_fmt} - {end_fmt}"
    except Exception:
        return window_utc

def validate_window_format(hhmm):
    try:
        s = str(hhmm).strip()
        if not re.match(r'^\d{3,4}$', s):
            return False
        val = int(s)
        return 0 <= val <= 2359
    except Exception:
        return False

def format_window(start, end):
    if not validate_window_format(start) or not validate_window_format(end):
        return None
    return f"{str(start).zfill(4)}-{str(end).zfill(4)} UTC"