"""Services for the Telegram bot."""

from .lms_api import lms_client, LMSAPIClient

__all__ = ["lms_client", "LMSAPIClient"]
