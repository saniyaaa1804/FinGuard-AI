
from langchain_ollama import ChatOllama

from finance_tools import (
    load_transactions,
    calculate_financial_summary,
    analyze_expenses,
    calculate_budget_status,
    generate_savings_suggestions
)

from guards.input_guard import check_user_input
from guards.privacy_guard import check_privacy
from guards.content_guard import validate_transaction_list
from guards.output_guard import filter_output

from utils.prompts import (
    SYSTEM_PROMPT,
    FINANCE_CONTEXT_PROMPT
)


class FinGuardAgent:

    def __init__(self):
        self.model = ChatOllama(
            model="qwen2.5:3b",
            temperature=0.1
        )

    def get_financial_data(self):

        transactions = load_transactions()

        validation = validate_transaction_list(transactions)

        if not validation["valid"]:
            raise ValueError(validation["message"])

        summary = calculate_financial_summary(transactions)

        categories = analyze_expenses(transactions)

        suggestions = generate_savings_suggestions(transactions)

        return {
            "transactions": transactions,
            "summary": summary,
            "categories": categories,
            "suggestions": suggestions
        }

    def analyze_finances(self):
        return self.get_financial_data()

    def check_budget(self, budget):

        data = self.get_financial_data()

        return calculate_budget_status(
            data["transactions"],
            budget
        )

    def ask_question(self, question):

        # Layer 1: Input validation
        input_result = check_user_input(question)

        if not input_result["safe"]:
            return input_result["message"]

        # Layer 2: Privacy protection
        privacy_result = check_privacy(question)

        safe_question = privacy_result["masked_text"]

        # Load verified financial data
        data = self.get_financial_data()

        summary = data["summary"]
        categories = data["categories"]

        # Explain how the figures should be interpreted
        interpretation = (
            "Total income is the sum of income transactions. "
            "Total expenses include every transaction marked expense. "
            "The Savings category contains a ₹3,000 transaction "
            "recorded as an expense and is already included in "
            "total expenses. Remaining balance is income minus "
            "recorded expenses. It is not proof of money actually "
            "deposited into a savings account."
        )

        # Build trusted financial context
        context = FINANCE_CONTEXT_PROMPT.format(
            financial_summary=summary,
            expense_categories=categories,
            interpretation=interpretation,
            question=safe_question
        )

        messages = [
            ("system", SYSTEM_PROMPT),
            ("human", context)
        ]

        try:

            response = self.model.invoke(messages)

            ai_response = response.content

            # Layer 3: Output validation
            safe_response = filter_output(ai_response)

            return safe_response

        except Exception as error:

            print("Ollama error:", error)

            return (
                "FinGuard AI could not connect to the local AI model. "
                "Please check whether Ollama is running."
            )
