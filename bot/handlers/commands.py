import httpx
from typing import Optional
from config import settings

def handle_start() -> str:
    """Handle /start command"""
    return (
        "🤖 Welcome to LMS Bot!\n\n"
        "Available commands:\n"
        "/start - Show this message\n"
        "/help - Show available commands\n"
        "/health - Check backend status\n"
        "/labs - List available labs\n"
        "/scores <lab> - Get scores for a lab\n"
        "/stats - Get submission statistics\n\n"
        "You can also ask questions in natural language!"
    )

def handle_help() -> str:
    """Handle /help command"""
    return (
        "📚 Available commands:\n\n"
        "/start - Welcome message\n"
        "/help - Show this help\n"
        "/health - Check if backend is working\n"
        "/labs - List all labs\n"
        "/scores <lab> - Get scores for a specific lab\n"
        "/stats - Get submission statistics\n\n"
        "💡 Tip: You can ask questions like:\n"
        "- 'Show me lab 4 scores'\n"
        "- 'How many students submitted lab 2?'"
    )

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

def handle_labs() -> str:
    """Handle /labs command - list available labs"""
    return "📋 Lab list will be available soon. (Not implemented yet)"

def handle_scores(lab: Optional[str] = None) -> str:
    """Handle /scores command - get scores for a lab"""
    if lab:
        return f"📊 Scores for {lab} will be shown soon. (Not implemented yet)"
    return "Please specify a lab: /scores lab-01"

def handle_stats() -> str:
    """Handle /stats command - get submission statistics"""
    return "📈 Statistics will be available soon. (Not implemented yet)"

def handle_unknown() -> str:
    """Handle unknown commands"""
    return "Unknown command. Use /help to see available commands."