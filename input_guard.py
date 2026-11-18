
import re


INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"ignore\s+the\s+system\s+prompt",
    r"reveal\s+(your\s+)?system\s+prompt",
    r"act\s+as\s+an?\s+unrestricted",
    r"bypass\s+(all\s+)?safety",
    r"disregard\s+(all\s+)?rules",
    r"developer\s+mode",
    r"override\s+(all\s+)?instructions"
]


def check_user_input(user_input):
    """Detect suspicious prompt injection attempts."""

    if not isinstance(user_input, str):
        return {
            "safe": False,
            "message": "Invalid input format."
        }

    if not user_input.strip():
        return {
            "safe": False,
            "message": "Please enter a question."
        }

    if len(user_input) > 2000:
        return {
            "safe": False,
            "message": "Input is too long. Maximum 2000 characters."
        }

    normalized_input = user_input.lower()

    for pattern in INJECTION_PATTERNS:

        if re.search(pattern, normalized_input):
            return {
                "safe": False,
                "message": (
                    "Potential prompt injection detected. "
                    "Your request was blocked."
                )
            }

    return {
        "safe": True,
        "message": "Input passed the security check."
    }
