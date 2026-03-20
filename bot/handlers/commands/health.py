"""Handler for /health command"""

import httpx
from config import settings


async def handle_health() -> str:
    """Handle /health command - check backend status"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.lms_api_url}/items/",
                headers={"Authorization": f"Bearer {settings.lms_api_key}"},
                timeout=5.0
            )
            if response.status_code == 200:
                return "✅ Backend is healthy and responding"
            else:
                return f"⚠️ Backend returned status {response.status_code}"
    except Exception as e:
        return f"❌ Cannot connect to backend: {str(e)}"
