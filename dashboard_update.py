import os
import requests
from datetime import datetime, timedelta
from notion_client import Client

# =========================================================
# AUTH
# =========================================================
NOTION_TOKEN = os.environ["NOTION_TOKEN"]
PAGE_ID = os.environ["NOTION_PAGE_ID"]

notion = Client(auth=NOTION_TOKEN)

# =========================================================
# TIME HANDLING (UTC reference + Arctic "yesterday")
# =========================================================
now = datetime.utcnow()
yesterday = now - timedelta(days=1)

date_str = yesterday.strftime("%Y-%m-%d")

# NASA Worldview (yesterday snapshot)
worldview_url = (
    "https://worldview.earthdata.nasa.gov/"
    f"?t={date_str}-T18%3A00%3A00Z"
)

# =========================================================
# TEMPERATURE MODULE (REAL DATA)
# =========================================================
def get_temperature():
    """
    Arctic temperature from Open-Meteo (ERA5-based reanalysis).
    Herschel Island coordinates.
    """

    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": 69.590,
            "longitude": -139.099,
            "current_weather": True
        }

        r = requests.get(url, params=params, timeout=10)
        data = r.json()

        temp = data["current_weather"]["temperature"]

        return {
            "temperature": temp,
            "source": "Open-Meteo (ERA5 reanalysis)",
            "status": "ok"
        }

    except Exception:
        return {
            "temperature": None,
            "source": "fallback (data unavailable)",
            "status": "missing"
        }

temp_data = get_temperature()

# =========================================================
# DASHBOARD TEXT
# =========================================================
temp_text = (
    f"Current air temperature: {temp_data['temperature']} °C\n"
    f"Source: {temp_data['source']}\n"
    f"Status: {temp_data['status']}"
)

# =========================================================
# NOTION BLOCKS
# =========================================================
blocks = [
    # TITLE
    {
        "object": "block",
        "type": "heading_1",
        "heading_1": {
            "rich_text": [{
                "type": "text",
                "text": {
                    "content": "Herschel Island Environmental Dashboard"
                }
            }]
        }
    },

    # TIMESTAMP
    {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{
                "type": "text",
                "text": {
                    "content": f"Last update (UTC): {now.strftime('%Y-%m-%d %H:%M')}"
                }
            }]
        }
    },

    {
        "object": "block",
        "type": "divider",
        "divider": {}
    },

    # =====================================================
    # SATELLITE SECTION
    # =====================================================
    {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{
                "type": "text",
                "text": {
                    "content": "🛰 Satellite (Worldview – previous day)"
                }
            }]
        }
    },

    {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{
                "type": "text",
                "text": {
                    "content": f"Automated observation for {date_str} (UTC reference)."
                }
            }]
        }
    },

    {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{
                "type": "text",
                "text": {
                    "content": worldview_url
                }
            }]
        }
    },

    # =====================================================
    # TEMPERATURE SECTION
    # =====================================================
    {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{
                "type": "text",
                "text": {
                    "content": "🌡 Air Temperature"
                }
            }]
        }
    },

    {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{
                "type": "text",
                "text": {
                    "content": temp_text
                }
            }]
        }
    },

    {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{
                "type": "text",
                "text": {
                    "content": "Note: Temperature is based on ERA5 reanalysis via Open-Meteo. Suitable for Arctic regional monitoring where in-situ data is intermittent."
                }
            }]
        }
    },

    # =====================================================
    # SEA ICE (placeholder next module)
    # =====================================================
    {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{
                "type": "text",
                "text": {
                    "content": "🧊 Sea Ice Conditions"
                }
            }]
        }
    },

    {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{
                "type": "text",
                "text": {
                    "content": "Next module: OSI SAF sea ice concentration (satellite-derived) + seasonal classification."
                }
            }]
        }
    },

    # =====================================================
    # TIDES / SEA LEVEL
    # =====================================================
    {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{
                "type": "text",
                "text": {
                    "content": "🌊 Tides & Sea Level"
                }
            }]
        }
    },

    {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{
                "type": "text",
                "text": {
                    "content": "Fisheries and Oceans Canada tide gauge (06525) + Copernicus sea level anomaly integration planned."
                }
            }]
        }
    },

    # FOOTER
    {
        "object": "block",
        "type": "divider",
        "divider": {}
    },

    {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{
                "type": "text",
                "text": {
                    "content": "All timestamps are in UTC. Interpretations should be referenced to Inuvik local time (seasonally UTC−7/−8)."
                }
            }]
        }
    }
]

# =========================================================
# CLEAR EXISTING PAGE CONTENT
# =========================================================
existing_blocks = notion.blocks.children.list(block_id=PAGE_ID)

for b in existing_blocks["results"]:
    notion.blocks.delete(block_id=b["id"])

# =========================================================
# PUSH NEW DASHBOARD
# =========================================================
notion.blocks.children.append(
    block_id=PAGE_ID,
    children=blocks
)

print("Dashboard updated successfully")
