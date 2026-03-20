"""Handler for /scores command"""

from typing import Optional


def handle_scores(lab: Optional[str] = None) -> str:
    """Handle /scores command - get scores for a lab"""
    if lab:
        return f"📊 Scores for {lab} will be shown soon. (Not implemented yet)"
    return "Please specify a lab: /scores lab-01"
