"""
config.py — Shingle Point site configuration.

Every value here is specific to this site. Shared logic lives in
dashboard_lib.py (the dashboard-lib repo, checked out alongside this one
in the GitHub Actions workflow — see .github/workflows/update.yml).

To add or remove a block from this site's dashboard, edit dashboard_update.py
in this repo (the SECTIONS assembly near the bottom) — not this file and
not dashboard_lib.py.
"""

import dashboard_lib as lib

# =========================================================
# CORE SITE IDENTITY
# =========================================================
SITE_DISPLAY_NAME = "Shingle Point"
LAT = 68.933333
LON = -137.2
TZ_NAME = "America/Inuvik"

# =========================================================
# MODIS / EPSG:3413 — see dashboard_lib's satellite module docstring for
# why these are precomputed constants, not live calculations.
# =========================================================
_HALF_WIDTH_M = 150_000
_MODIS_OVERSIZE_HALF_WIDTH_M = _HALF_WIDTH_M * lib.MODIS_OVERSIZE_FACTOR

# Computed via lib.compute_3413_center(LAT, LON) — verified against
# pyproj to sub-meter precision (see project history).
MODIS_CENTER_X, MODIS_CENTER_Y = -2305418, 88565

MODIS_BBOX_3413 = (
    f"{MODIS_CENTER_X - _MODIS_OVERSIZE_HALF_WIDTH_M:.0f},{MODIS_CENTER_Y - _MODIS_OVERSIZE_HALF_WIDTH_M:.0f},"
    f"{MODIS_CENTER_X + _MODIS_OVERSIZE_HALF_WIDTH_M:.0f},{MODIS_CENTER_Y + _MODIS_OVERSIZE_HALF_WIDTH_M:.0f}"
)

# PROVISIONAL — derived geometrically, not yet empirically reconfirmed
# since the library's generalization. Verify visually after a real run:
# if the coastline orientation looks rotated relative to a real map,
# adjust this value (see rotate_to_north_up's docstring in dashboard_lib
# for the empirical-verification approach this needs).
MODIS_ROTATION_DEG = 92.0

# =========================================================
# UTM (for Sentinel-1) — Shingle Point is zone 8, NOT the same zone as
# Herschel Island (zone 7), despite being only ~130km away. Verified via
# lib.compute_utm_zone(LON) — see dashboard_lib's satellite module
# docstring for why this must be checked per site, not assumed.
# =========================================================
UTM_ZONE = 8
UTM_EPSG = "32608"
UTM_CENTER_X, UTM_CENTER_Y = lib.latlon_to_utm(LAT, LON, zone=UTM_ZONE)

# =========================================================
# MAP ANNOTATION — markers shown on both the MODIS and Sentinel-1 images.
# Format: (lat, lon, label) or (lat, lon, label, text_dy) or
# (lat, lon, label, text_dy, text_dx) — see annotate_modis_image's
# docstring in dashboard_lib for the tuple format and text_dx/dy meaning.
# =========================================================
MAP_POINTS = [
    (LAT, LON, SITE_DISPLAY_NAME, -28),
    (69.568861, -138.911754, "Qikiqtaruk Herschel Island", -10),
    (68.226653, -135.003294, "Aklavik", -10),
    (68.360741, -133.723022, "Inuvik", -10, -90),
]

# Yukon/Alaska international border — relevant here since Shingle Point
# sits close to it. A site further from any such border can simply pass
# reference_lines=None to the satellite section builders.
MAP_REFERENCE_LINES = [
    (60.0, -141.0, 69.65, -141.0, "Yukon/Alaska border"),
]

COASTLINE_GEOJSON_PATH = "coastline_data.geojson"  # relative to this repo's root

# =========================================================
# TIDE STATION (DFO IWLS)
# =========================================================
TIDE_STATION_CODE = "06505"
TIDE_STATION_NAME = "Shingle Point"

# =========================================================
# MARINE FORECAST ZONE (Environment Canada)
# =========================================================
MARINE_ZONE_ID = "16000"
MARINE_ZONE_NAME = "Yukon Coast"

# =========================================================
# TOTAL WATER LEVEL (TOPAZ6) — yearly mean computed once via
# build_yearly_mean_helper_script.py in this repo, not live every run.
# =========================================================
WATER_LEVEL_YEARLY_MEAN = -0.2668  # computed 2026-06-25

# =========================================================
# HYDROMETRIC STATIONS — a site can list any number of these; each
# becomes its own section via lib.build_hydrometric_section. Shingle
# Point has one (Napoiak Channel); a future site might have several, or
# none at all (just use an empty list).
# =========================================================
HYDROMETRIC_STATIONS = [
    {
        "station_id": "10MC023",
        "provterr": "NT",
        "river_name": "Mackenzie River, Napoiak Channel above Shallow Bay",
        "heading": "💧 Napoiak Channel Water Level — Mackenzie River above Shallow Bay",
    },
]

# =========================================================
# INSTITUTIONAL BRANDING
# =========================================================
LOGO_URL = "https://www.awi.de/_assets/978631966794c5093250775de182779d/Images/AWI/awi_logo.svg"
INSTITUTION_TEXT = (
    "This dashboard is provided by the Alfred Wegener Institute Helmholtz Centre "
    "for Polar and Marine Research."
)
