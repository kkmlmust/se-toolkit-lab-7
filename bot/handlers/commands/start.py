"""Handler for /start command"""


def handle_start() -> str:
    """Handle /start command - show welcome message"""
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
