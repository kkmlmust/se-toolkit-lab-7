#!/usr/bin/env python3
"""
LMS Telegram Bot - Entry Point
Supports --test mode for offline verification and LLM intent routing.
"""

import sys
import asyncio
import argparse
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from handlers.commands import (
    handle_start, handle_help, handle_health,
    handle_labs, handle_scores, handle_stats, handle_unknown
)
from services import route_intent
from config import settings


# Inline keyboard buttons for common actions
START_KEYBOARD = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("📚 Available Labs", callback_data="labs"),
        InlineKeyboardButton("❤️ Health Check", callback_data="health"),
    ],
    [
        InlineKeyboardButton("📊 Scores", callback_data="scores"),
        InlineKeyboardButton("❓ Help", callback_data="help"),
    ],
])

HELP_KEYBOARD = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("📚 List Labs", callback_data="labs"),
    ],
    [
        InlineKeyboardButton("📊 Lab 4 Scores", callback_data="scores_lab-04"),
    ],
    [
        InlineKeyboardButton("❤️ Health", callback_data="health"),
    ],
])


async def test_mode(command: str) -> None:
    """Run bot in test mode - print response to stdout without Telegram"""
    # Parse command
    parts = command.strip().split()
    cmd = parts[0]
    args = parts[1:] if len(parts) > 1 else []

    # Check if it's a slash command
    if cmd.startswith("/"):
        # Route to appropriate handler
        if cmd == "/start":
            response = handle_start()
        elif cmd == "/help":
            response = handle_help()
        elif cmd == "/health":
            response = await handle_health()
        elif cmd == "/labs":
            response = await handle_labs()
        elif cmd == "/scores":
            lab = args[0] if args else None
            response = await handle_scores(lab)
        elif cmd == "/stats":
            response = handle_stats()
        else:
            response = handle_unknown()
    else:
        # Natural language query - use intent router
        full_message = command.strip()
        response = await route_intent(full_message, debug=True)

    print(response)


async def handle_health_command(update, context) -> None:
    """Telegram handler for /health command"""
    response = await handle_health()
    await update.message.reply_text(response)


async def handle_labs_command(update, context) -> None:
    """Telegram handler for /labs command"""
    response = await handle_labs()
    await update.message.reply_text(response)


async def handle_scores_command(update, context) -> None:
    """Telegram handler for /scores command"""
    lab = context.args[0] if context.args else None
    response = await handle_scores(lab)
    await update.message.reply_text(response)


async def handle_start_command(update, context) -> None:
    """Telegram handler for /start command with inline keyboard"""
    response = handle_start()
    await update.message.reply_text(response, reply_markup=START_KEYBOARD)


async def handle_help_command(update, context) -> None:
    """Telegram handler for /help command with inline keyboard"""
    response = handle_help()
    await update.message.reply_text(response, reply_markup=HELP_KEYBOARD)


async def handle_callback_query(update, context) -> None:
    """Handle inline keyboard button clicks"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "labs":
        response = await handle_labs()
    elif data == "health":
        response = await handle_health()
    elif data == "help":
        response = handle_help()
    elif data == "scores":
        response = "Please specify a lab: /scores lab-01"
    elif data.startswith("scores_"):
        lab = data.replace("scores_", "")
        response = await handle_scores(lab)
    else:
        response = "Unknown action."
    
    await query.edit_message_text(response)


async def handle_message(update, context) -> None:
    """Handle plain text messages with LLM intent routing"""
    user_message = update.message.text
    
    if not user_message:
        return
    
    # Skip if it looks like a command (commands are handled separately)
    if user_message.startswith("/"):
        return
    
    # Use LLM intent router
    try:
        response = await route_intent(user_message, debug=True)
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text(f"❌ Error processing your message: {str(e)}")


def run_telegram_bot() -> None:
    """Run the bot in normal Telegram mode"""
    # Create application
    app = Application.builder().token(settings.bot_token).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", handle_start_command))
    app.add_handler(CommandHandler("help", handle_help_command))
    app.add_handler(CommandHandler("health", handle_health_command))
    app.add_handler(CommandHandler("labs", handle_labs_command))
    app.add_handler(CommandHandler("scores", handle_scores_command))
    app.add_handler(CommandHandler("stats", lambda u, c: u.message.reply_text(handle_stats())))
    
    # Register callback query handler for inline buttons
    app.add_handler(MessageHandler(filters.StatusUpdate.CALLBACK_QUERY, handle_callback_query))
    
    # Register message handler for plain text (intent routing)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start bot
    print("Starting Telegram bot...")
    app.run_polling(allowed_updates=["message"])


def main():
    parser = argparse.ArgumentParser(description="LMS Telegram Bot")
    parser.add_argument("--test", help="Run in test mode with a command", metavar="COMMAND")
    args = parser.parse_args()

    if args.test:
        asyncio.run(test_mode(args.test))
    else:
        run_telegram_bot()


if __name__ == "__main__":
    main()
