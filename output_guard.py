
import re


MAX_OUTPUT_LENGTH = 5000


UNSAFE_PATTERNS = [
    r"guaranteed\s+(profit|returns|income)",
    r"risk[- ]free\s+(investment|profit|returns)",
    r"100%\s+guaranteed",
    r"you\s+will\s+definitely\s+(get|earn|make)",
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"reveal\s+(your\s+)?system\s+prompt",
]


def check_output(response):
    """Validate AI-generated financial responses."""

    if not isinstance(response, str):
        return {
            "safe": False,
            "message": "Invalid AI response format.",
            "cleaned_output": ""
        }

    response = response.strip()

    if not response:
        return {
            "safe": False,
            "message": "AI response is empty.",
            "cleaned_output": ""
        }

    if len(response) > MAX_OUTPUT_LENGTH:
        return {
            "safe": False,
            "message": "AI response exceeds the allowed length.",
            "cleaned_output": ""
        }

    for pattern in UNSAFE_PATTERNS:

        if re.search(pattern, response, re.IGNORECASE):
            return {
                "safe": False,
                "message": (
                    "Potentially unsafe financial content detected."
                ),
                "cleaned_output": ""
            }

    return {
        "safe": True,
        "message": "AI response passed output validation.",
        "cleaned_output": response
    }


def filter_output(response):
    """Return only responses that pass output validation."""

    result = check_output(response)

    if result["safe"]:
        return result["cleaned_output"]

    return (
        "Sorry, this response could not be displayed because "
        "it did not pass the safety checks. "
        "Please try asking a different question."
    )
