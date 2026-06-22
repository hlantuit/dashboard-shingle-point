from notion_client import Client
from datetime import datetime

NOTION_TOKEN = "PUT_YOUR_TOKEN_HERE"
PAGE_ID = "PUT_YOUR_PAGE_ID_HERE"

notion = Client(auth=NOTION_TOKEN)

now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

notion.pages.update(
    page_id=PAGE_ID,
    properties={
        "title": {
            "title": [
                {
                    "text": {
                        "content": f"Herschel Dashboard (updated {now})"
                    }
                }
            ]
        }
    }
)

print("Updated Notion")
