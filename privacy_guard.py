
import re


PRIVACY_PATTERNS = {
    "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",

    "PHONE": r"(?<!\d)(?:\+91[-\s]?)?[6-9]\d{9}(?!\d)",

    "AADHAAR_LIKE": r"(?<!\d)\d{4}[-\s]?\d{4}[-\s]?\d{4}(?!\d)",

    "CARD_LIKE": r"(?<!\d)(?:\d[ -]?){15}\d(?!\d)"
}


def detect_sensitive_data(text):
    """Detect possible sensitive information in text."""

    if not isinstance(text, str):
        return []

    detected = []

    for data_type, pattern in PRIVACY_PATTERNS.items():

        matches = re.findall(pattern, text)

        if matches:
            detected.append({
                "type": data_type,
                "count": len(matches)
            })

    return detected


def mask_sensitive_data(text):
    """Mask sensitive information before AI processing."""

    if not isinstance(text, str):
        raise ValueError("Input must be text.")

    masked_text = text

    for data_type, pattern in PRIVACY_PATTERNS.items():

        masked_text = re.sub(
            pattern,
            f"[{data_type}_REDACTED]",
            masked_text
        )

    return masked_text


def check_privacy(text):
    """Return privacy check results."""

    detected = detect_sensitive_data(text)

    masked_text = mask_sensitive_data(text)

    return {
        "safe": len(detected) == 0,
        "detected": detected,
        "masked_text": masked_text,
        "message": (
            "Sensitive information detected and masked."
            if detected
            else "No sensitive patterns detected."
        )
    }
