"""Handler for /health command"""

import httpx
from config import settings
from services.lms_api import lms_client


async def handle_health() -> str:
    """Handle /health command - check backend status"""
    try:
        items = await lms_client.get_items()
        item_count = len(items)
        labs = [i for i in items if i.get("type") == "lab"]
        lab_count = len(labs)
        return f"✅ Backend is healthy. {item_count} items available ({lab_count} labs)."
    except httpx.ConnectError as e:
        return f"❌ Backend error: connection refused ({settings.lms_api_url}). Check that the services are running."
    except httpx.HTTPStatusError as e:
        return f"❌ Backend error: HTTP {e.response.status_code} {e.response.reason_phrase}. The backend service may be down."
    except httpx.HTTPError as e:
        return f"❌ Backend error: {str(e)}"
    except Exception as e:
        return f"❌ Backend error: {str(e)}"
