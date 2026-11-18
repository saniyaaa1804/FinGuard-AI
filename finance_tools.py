
import csv
from pathlib import Path


DATA_FILE = Path(__file__).parent / "data" / "sample_transactions.csv"

REQUIRED_COLUMNS = {
    "date",
    "description",
    "category",
    "type",
    "amount"
}


def load_transactions(file_path=DATA_FILE):
    """Load and validate transactions from a CSV file."""

    transactions = []

    try:
        with open(
            file_path,
            mode="r",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            reader = csv.DictReader(file)

            if not reader.fieldnames:
                raise ValueError("CSV file is empty or has no header.")

            # Normalize column names
            original_headers = reader.fieldnames
            normalized_headers = [
                header.strip().lower() for header in original_headers
            ]

            reader.fieldnames = normalized_headers

            # Validate required columns
            if not REQUIRED_COLUMNS.issubset(set(normalized_headers)):
                raise ValueError(
                    f"CSV is missing required columns. "
                    f"Found: {normalized_headers}"
                )

            for row_number, row in enumerate(reader, start=2):

                transaction_type = row["type"].strip().lower()

                if transaction_type not in {"income", "expense"}:
                    raise ValueError(
                        f"Invalid transaction type on row {row_number}."
                    )

                try:
                    amount = float(row["amount"])
                except (ValueError, TypeError):
                    raise ValueError(
                        f"Invalid amount on row {row_number}."
                    )

                if amount < 0:
                    raise ValueError(
                        f"Negative amount on row {row_number}."
                    )

                transactions.append({
                    "date": row["date"].strip(),
                    "description": row["description"].strip(),
                    "category": row["category"].strip(),
                    "type": transaction_type,
                    "amount": amount
                })

    except FileNotFoundError:
        raise FileNotFoundError(
            f"Transaction file not found: {file_path}"
        )

    except (OSError, csv.Error) as error:
        raise ValueError(
            f"Unable to read transaction file: {error}"
        ) from error

    return transactions


def calculate_financial_summary(transactions):
    """Calculate income, expenses and remaining balance."""

    income = sum(
        item["amount"]
        for item in transactions
        if item["type"].lower() == "income"
    )

    expenses = sum(
        item["amount"]
        for item in transactions
        if item["type"].lower() == "expense"
    )

    savings = income - expenses

    savings_rate = (
        (savings / income) * 100 if income > 0 else 0
    )

    return {
        "total_income": round(income, 2),
        "total_expenses": round(expenses, 2),
        "remaining_balance": round(savings, 2),
        "savings_rate": round(savings_rate, 2)
    }


def analyze_expenses(transactions):
    """Calculate expenses category-wise."""

    categories = {}

    for item in transactions:

        if item["type"].lower() == "expense":

            category = item["category"]

            categories[category] = (
                categories.get(category, 0) + item["amount"]
            )

    result = [
        {
            "category": category,
            "amount": round(amount, 2)
        }
        for category, amount in sorted(
            categories.items(),
            key=lambda entry: entry[1],
            reverse=True
        )
    ]

    return result


def calculate_budget_status(transactions, monthly_budget):
    """Compare expenses against the monthly budget."""

    if monthly_budget <= 0:
        raise ValueError("Budget must be greater than zero.")

    summary = calculate_financial_summary(transactions)

    expenses = summary["total_expenses"]

    remaining = monthly_budget - expenses

    usage = (expenses / monthly_budget) * 100

    return {
        "monthly_budget": round(float(monthly_budget), 2),
        "total_expenses": expenses,
        "remaining_budget": round(remaining, 2),
        "budget_usage": round(usage, 2),
        "status": (
            "Over Budget"
            if remaining < 0
            else "Within Budget"
        )
    }


def generate_savings_suggestions(transactions):
    """Generate rule-based savings suggestions."""

    categories = analyze_expenses(transactions)

    if not categories:
        return [
            "Add expense transactions to receive savings suggestions."
        ]

    highest = categories[0]

    summary = calculate_financial_summary(transactions)

    suggestions = [
        (
            f"Your highest spending category is "
            f"{highest['category']} at ₹{highest['amount']:.2f}."
        ),
        (
            "Review non-essential expenses and consider "
            "setting category-wise spending limits."
        )
    ]

    if summary["remaining_balance"] < 0:

        suggestions.append(
            "Your expenses exceed your income. "
            "Review your spending and essential costs."
        )

    else:

        suggestions.append(
            "Consider setting aside part of your remaining "
            "balance as savings."
        )

    return suggestions
