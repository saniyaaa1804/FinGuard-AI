
"""
FinGuard AI - Financial Calculation Utilities

All calculations are performed using Python.
The AI model is used only to explain the calculated results.
"""


def calculate_percentage(part, total):
    """Calculate percentage safely."""

    if total <= 0:
        return 0.0

    return round((part / total) * 100, 2)


def calculate_savings_rate(income, expenses):
    """Calculate the remaining-balance percentage of income."""

    if income <= 0:
        return 0.0

    remaining_balance = income - expenses

    return calculate_percentage(
        remaining_balance,
        income
    )


def calculate_remaining_balance(income, expenses):
    """Calculate income minus recorded expenses."""

    return round(income - expenses, 2)


def calculate_category_totals(transactions):
    """Calculate expense totals for each category."""

    category_totals = {}

    for transaction in transactions:

        if transaction["type"].lower() == "expense":

            category = transaction["category"]

            amount = float(transaction["amount"])

            category_totals[category] = (
                category_totals.get(category, 0) + amount
            )

    return {
        category: round(amount, 2)
        for category, amount in sorted(
            category_totals.items(),
            key=lambda item: item[1],
            reverse=True
        )
    }
