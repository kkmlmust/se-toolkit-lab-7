"""Handler for /help command"""


def handle_help() -> str:
    """Handle /help command - show available commands"""
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
