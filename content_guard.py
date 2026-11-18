
import re


ALLOWED_TRANSACTION_TYPES = {"income", "expense"}

MAX_DESCRIPTION_LENGTH = 200

SUSPICIOUS_CONTENT_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"reveal\s+(your\s+)?system\s+prompt",
    r"ignore\s+the\s+system\s+prompt",
    r"execute\s+this\s+command",
    r"send\s+(all\s+)?data\s+to",
    r"delete\s+(all\s+)?records",
]


def validate_description(description):
    """Validate an untrusted transaction description."""

    if not isinstance(description, str):
        return {
            "valid": False,
            "message": "Description must be text."
        }

    description = description.strip()

    if not description:
        return {
            "valid": False,
            "message": "Transaction description cannot be empty."
        }

    if len(description) > MAX_DESCRIPTION_LENGTH:
        return {
            "valid": False,
            "message": "Description exceeds the 200-character limit."
        }

    for pattern in SUSPICIOUS_CONTENT_PATTERNS:

        if re.search(pattern, description, re.IGNORECASE):
            return {
                "valid": False,
                "message": "Suspicious instructions detected in content."
            }

    return {
        "valid": True,
        "message": "Transaction description is valid."
    }


def validate_transaction(transaction):
    """Validate the structure and values of a transaction."""

    if not isinstance(transaction, dict):
        return {
            "valid": False,
            "message": "Transaction must be a dictionary."
        }

    required_fields = {
        "date",
        "description",
        "category",
        "type",
        "amount"
    }

    if not required_fields.issubset(transaction.keys()):
        return {
            "valid": False,
            "message": "Transaction is missing required fields."
        }

    description_result = validate_description(
        transaction["description"]
    )

    if not description_result["valid"]:
        return description_result

    if not isinstance(transaction["category"], str) or not transaction["category"].strip():
        return {
            "valid": False,
            "message": "Invalid transaction category."
        }

    transaction_type = str(transaction["type"]).strip().lower()

    if transaction_type not in ALLOWED_TRANSACTION_TYPES:
        return {
            "valid": False,
            "message": "Invalid transaction type."
        }

    try:
        amount = float(transaction["amount"])
    except (ValueError, TypeError):
        return {
            "valid": False,
            "message": "Transaction amount must be numeric."
        }

    if amount < 0:
        return {
            "valid": False,
            "message": "Transaction amount cannot be negative."
        }

    return {
        "valid": True,
        "message": "Transaction passed content validation."
    }


def validate_transaction_list(transactions):
    """Validate a complete list of transactions."""

    if not isinstance(transactions, list):
        return {
            "valid": False,
            "message": "Expected a list of transactions."
        }

    if not transactions:
        return {
            "valid": False,
            "message": "No transactions available."
        }

    for index, transaction in enumerate(transactions):

        result = validate_transaction(transaction)

        if not result["valid"]:
            return {
                "valid": False,
                "message": f"Transaction {index + 1}: {result['message']}"
            }

    return {
        "valid": True,
        "message": "All transactions passed content validation."
    }
