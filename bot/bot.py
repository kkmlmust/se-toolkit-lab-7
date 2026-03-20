#!/usr/bin/env python3
"""
LMS Telegram Bot - Entry Point
Supports --test mode for offline verification
"""

import sys
import asyncio
import argparse
from telegram.ext import Application, CommandHandler

from handlers.commands import (
    handle_start, handle_help, handle_health,
    handle_labs, handle_scores, handle_stats, handle_unknown
)
from config import settings


async def test_mode(command: str) -> None:
    """Run bot in test mode - print response to stdout without Telegram"""
    # Parse command
    parts = command.strip().split()
    cmd = parts[0]
    args = parts[1:] if len(parts) > 1 else []

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


def run_telegram_bot() -> None:
    """Run the bot in normal Telegram mode"""
    # Create application
    app = Application.builder().token(settings.bot_token).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", lambda u, c: u.message.reply_text(handle_start())))
    app.add_handler(CommandHandler("help", lambda u, c: u.message.reply_text(handle_help())))
    app.add_handler(CommandHandler("health", handle_health_command))
    app.add_handler(CommandHandler("labs", handle_labs_command))
    app.add_handler(CommandHandler("scores", handle_scores_command))
    app.add_handler(CommandHandler("stats", lambda u, c: u.message.reply_text(handle_stats())))

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
