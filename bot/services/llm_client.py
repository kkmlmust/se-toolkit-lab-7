"""LLM Client for intent routing with tool calling support."""

import httpx
from typing import Any, Optional
from config import settings


# Define all 9 backend endpoints as LLM tools
TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "get_items",
            "description": "Get list of all labs and tasks in the system. Use this to discover what labs are available.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_learners",
            "description": "Get list of enrolled students and their groups. Use this to find student information.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_scores",
            "description": "Get score distribution (4 buckets) for a specific lab.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {"type": "string", "description": "Lab identifier, e.g. 'lab-01' or '4'"}
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_pass_rates",
            "description": "Get per-task average pass rates and attempt counts for a specific lab.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {"type": "string", "description": "Lab identifier, e.g. 'lab-01' or '4'"}
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_timeline",
            "description": "Get submission timeline (submissions per day) for a specific lab.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {"type": "string", "description": "Lab identifier, e.g. 'lab-01' or '4'"}
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_groups",
            "description": "Get per-group performance and student counts for a specific lab.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {"type": "string", "description": "Lab identifier, e.g. 'lab-01' or '4'"}
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_top_learners",
            "description": "Get top N learners by score for a specific lab.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {"type": "string", "description": "Lab identifier, e.g. 'lab-01' or '4'"},
                    "limit": {"type": "integer", "description": "Number of top learners to return (default: 5)"}
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_completion_rate",
            "description": "Get completion rate percentage for a specific lab.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {"type": "string", "description": "Lab identifier, e.g. 'lab-01' or '4'"}
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "trigger_sync",
            "description": "Trigger ETL pipeline sync to refresh data from the autochecker.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
]

# System prompt for the LLM
SYSTEM_PROMPT = """You are a helpful assistant for a Learning Management System (LMS). 
You have access to tools that let you query data about labs, students, scores, and analytics.

When the user asks a question:
1. Think about what information you need
2. Call the appropriate tools to get that information
3. Use the tool results to provide a helpful, accurate answer

Available tools:
- get_items: List all labs and tasks
- get_learners: List enrolled students
- get_scores: Score distribution for a lab
- get_pass_rates: Per-task pass rates for a lab
- get_timeline: Submission timeline for a lab
- get_groups: Per-group performance for a lab
- get_top_learners: Top students for a lab
- get_completion_rate: Completion percentage for a lab
- trigger_sync: Refresh data from autochecker

If the user's message is a greeting or doesn't require data, respond naturally without using tools.
If you're unsure what the user wants, ask for clarification.
Always provide helpful context about what you can do if the user seems confused."""


class LLMClient:
    """Client for LLM API with tool calling support."""

    def __init__(self) -> None:
        self.api_key = settings.llm_api_key
        self.base_url = settings.llm_api_base_url
        self.model = settings.llm_api_model

    async def chat(
        self,
        messages: list[dict[str, Any]],
        tools: Optional[list[dict[str, Any]]] = None,
    ) -> dict[str, Any]:
        """Send a chat request to the LLM with optional tool definitions."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
        }
        
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()


# Global client instance
llm_client = LLMClient()
