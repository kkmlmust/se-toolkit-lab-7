"""Command handlers for the Telegram bot.

Handlers are plain functions separated from the Telegram transport layer.
They can be called from --test mode, unit tests, or Telegram.
"""

from .start import handle_start
from .help import handle_help
from .health import handle_health
from .labs import handle_labs
from .scores import handle_scores
from .stats import handle_stats
from .unknown import handle_unknown

__all__ = [
    "handle_start",
    "handle_help",
    "handle_health",
    "handle_labs",
    "handle_scores",
    "handle_stats",
    "handle_unknown",
]
