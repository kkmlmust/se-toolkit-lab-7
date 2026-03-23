"""Helper utilities for the bot."""


def normalize_lab_id(lab_input: str) -> str:
    """
    Normalize lab identifier to just the number.

    This is a utility function used AFTER the LLM has already decided which tool to call.
    The LLM decides which tool to use - this just formats the arguments.
    """
    if not lab_input:
        return ""

    # Extract digits from input like "lab-04", "lab-4", "4", "Lab 04"
    # This is purely for argument formatting, not for routing decisions
    lab_str = str(lab_input)
    digits = "".join(c for c in lab_str if c.isdigit())
    return digits if digits else lab_str
