"""Handler for /labs command"""

import httpx
from services.lms_api import lms_client


async def handle_labs() -> str:
    """Handle /labs command - list available labs"""
    try:
        items = await lms_client.get_items()
        labs = [i for i in items if i.get("type") == "lab"]
        
        if not labs:
            return "📋 No labs found in the system."
        
        lines = ["📚 Available labs:"]
        for lab in labs:
            title = lab.get("title", "Unknown Lab")
            lines.append(f"- {title}")
        
        return "\n".join(lines)
    except httpx.ConnectError:
        return "❌ Backend error: connection refused. Check that the services are running."
    except httpx.HTTPStatusError as e:
        return f"❌ Backend error: HTTP {e.response.status_code} {e.response.reason_phrase}."
    except httpx.HTTPError as e:
        return f"❌ Backend error: {str(e)}"
    except Exception as e:
        return f"❌ Backend error: {str(e)}"
