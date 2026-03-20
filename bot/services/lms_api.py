"""LMS API Client for fetching data from the backend."""

import httpx
from typing import Any
from config import settings


class LMSAPIClient:
    """Client for the LMS backend API."""

    def __init__(self) -> None:
        self.base_url = settings.lms_api_url
        self.api_key = settings.lms_api_key
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    async def _request(self, method: str, endpoint: str, **kwargs: Any) -> httpx.Response:
        """Make an API request with error handling."""
        url = f"{self.base_url}{endpoint}"
        headers = {**self.headers, **kwargs.get("headers", {})}
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, headers=headers, **kwargs)
            response.raise_for_status()
            return response

    async def get_items(self) -> list[dict[str, Any]]:
        """Fetch all items (labs, tasks, etc.) from the backend."""
        response = await self._request("GET", "/items/")
        return response.json()

    async def get_learners(self) -> list[dict[str, Any]]:
        """Fetch all learners from the backend."""
        response = await self._request("GET", "/learners/")
        return response.json()

    async def get_pass_rates(self, lab: str) -> list[dict[str, Any]]:
        """Fetch pass rates for a specific lab."""
        response = await self._request("GET", "/analytics/pass-rates", params={"lab": lab})
        return response.json()

    async def get_scores(self, lab: str) -> list[dict[str, Any]]:
        """Fetch score distribution for a specific lab."""
        response = await self._request("GET", "/analytics/scores", params={"lab": lab})
        return response.json()

    async def get_timeline(self, lab: str) -> list[dict[str, Any]]:
        """Fetch submission timeline for a specific lab."""
        response = await self._request("GET", "/analytics/timeline", params={"lab": lab})
        return response.json()

    async def get_groups(self, lab: str) -> list[dict[str, Any]]:
        """Fetch per-group performance for a specific lab."""
        response = await self._request("GET", "/analytics/groups", params={"lab": lab})
        return response.json()

    async def get_top_learners(self, lab: str, limit: int = 5) -> list[dict[str, Any]]:
        """Fetch top learners for a specific lab."""
        response = await self._request("GET", "/analytics/top-learners", params={"lab": lab, "limit": limit})
        return response.json()

    async def get_completion_rate(self, lab: str) -> dict[str, Any]:
        """Fetch completion rate for a specific lab."""
        response = await self._request("GET", "/analytics/completion-rate", params={"lab": lab})
        return response.json()

    async def sync_pipeline(self) -> dict[str, Any]:
        """Trigger ETL pipeline sync."""
        response = await self._request("POST", "/pipeline/sync", json={})
        return response.json()


# Global client instance
lms_client = LMSAPIClient()
