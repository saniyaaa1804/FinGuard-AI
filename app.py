
import streamlit as st
import plotly.graph_objects as go
from datetime import date

from agent import FinGuardAgent

from database import (
    initialize_database,
    get_all_transactions,
    add_transaction,
    import_transactions
)

from finance_tools import (
    load_transactions,
    calculate_financial_summary,
    analyze_expenses,
    calculate_budget_status,
    generate_savings_suggestions
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="FinGuard AI",
    page_icon="💰",
    layout="wide"
)


# --------------------------------------------------
# INITIALIZATION
# --------------------------------------------------

initialize_database()


@st.cache_resource
def get_agent():
    return FinGuardAgent()


agent = get_agent()


def load_database_transactions():

    transactions = get_all_transactions()

    if not transactions:
        sample_transactions = load_transactions()
        import_transactions(sample_transactions)
        transactions = get_all_transactions()

    return transactions


load_database_transactions()


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def format_inr(amount):
    return f"₹{amount:,.2f}"


def get_current_data():
    return get_all_transactions()


# --------------------------------------------------
# CUSTOM STYLING
# --------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #f7f9fc;
}

[data-testid="stMetric"] {
    background-color: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
}

div.stButton > button {
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("💰 FinGuard AI")
st.sidebar.caption("Your Personal Finance Assistant")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Transactions",
        "Budget Planner",
        "AI Finance Assistant",
        "Safety Center"
    ]
)

st.sidebar.divider()
st.sidebar.success("Local AI: Qwen 2.5 3B")
st.sidebar.caption("Powered by Python, SQLite and Ollama")


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if page == "Dashboard":

    st.title("📊 Financial Dashboard")

    st.write(
        "Get an overview of your income, expenses and financial health."
    )

    transactions = get_current_data()

    if not transactions:
        st.info("No transactions available.")
        st.stop()

    summary = calculate_financial_summary(transactions)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Income", format_inr(summary["total_income"]))
    col2.metric("Total Expenses", format_inr(summary["total_expenses"]))
    col3.metric("Remaining Balance", format_inr(summary["remaining_balance"]))
    col4.metric("Savings Rate", f'{summary["savings_rate"]}%')

    st.divider()

    st.subheader("Expense Analysis")

    categories = analyze_expenses(transactions)

    if categories:

        chart_col1, chart_col2 = st.columns(2)

        category_names = [
            item["category"] for item in categories
        ]

        category_amounts = [
            item["amount"] for item in categories
        ]

        with chart_col1:

            pie_chart = go.Figure(
                data=[
                    go.Pie(
                        labels=category_names,
                        values=category_amounts,
                        hole=0.4
                    )
                ]
            )

            pie_chart.update_layout(
                title="Expense Distribution",
                template="plotly_white"
            )

            st.plotly_chart(
                pie_chart,
                use_container_width=True
            )

        with chart_col2:

            bar_chart = go.Figure(
                data=[
                    go.Bar(
                        x=category_names,
                        y=category_amounts
                    )
                ]
            )

            bar_chart.update_layout(
                title="Category-wise Expenses",
                xaxis_title="Category",
                yaxis_title="Amount (₹)",
                template="plotly_white"
            )

            st.plotly_chart(
                bar_chart,
                use_container_width=True
            )

    st.subheader("Recent Transactions")

    for transaction in transactions[:5]:

        st.write(
            f'**{transaction["description"]}** — '
            f'{transaction["category"]} — '
            f'{format_inr(transaction["amount"])} '
            f'({transaction["type"].title()})'
        )

    st.divider()

    st.subheader("AI Savings Suggestions")

    for suggestion in generate_savings_suggestions(transactions):
        st.info(suggestion)


# --------------------------------------------------
# TRANSACTIONS
# --------------------------------------------------

elif page == "Transactions":

    st.title("🧾 Transaction Management")

    st.write("Add and review your income and expenses.")

    with st.form("transaction_form"):

        col1, col2 = st.columns(2)

        with col1:

            transaction_date = st.date_input(
                "Transaction Date",
                value=date.today()
            )

            description = st.text_input("Description")

            category = st.selectbox(
                "Category",
                [
                    "Salary",
                    "Freelance",
                    "Housing",
                    "Food",
                    "Utilities",
                    "Fuel",
                    "Transport",
                    "Healthcare",
                    "Shopping",
                    "Entertainment",
                    "Savings",
                    "Other"
                ]
            )

        with col2:

            transaction_type = st.selectbox(
                "Transaction Type",
                ["income", "expense"]
            )

            amount = st.number_input(
                "Amount (₹)",
                min_value=0.0,
                step=100.0
            )

        submitted = st.form_submit_button("Add Transaction")

        if submitted:

            if not description.strip():

                st.error("Please enter a description.")

            elif amount <= 0:

                st.error("Amount must be greater than zero.")

            else:

                try:

                    add_transaction(
                        str(transaction_date),
                        description.strip(),
                        category,
                        transaction_type,
                        amount
                    )

                    st.success("Transaction added successfully!")
                    st.rerun()

                except Exception as error:

                    st.error(f"Unable to add transaction: {error}")

    st.divider()

    st.subheader("All Transactions")

    transactions = get_current_data()

    if transactions:

        for transaction in transactions:

            st.write(
                f'**{transaction["date"]}** | '
                f'{transaction["description"]} | '
                f'{transaction["category"]} | '
                f'{transaction["type"].title()} | '
                f'{format_inr(transaction["amount"])}'
            )

    else:

        st.info("No transactions found.")


# --------------------------------------------------
# BUDGET PLANNER
# --------------------------------------------------

elif page == "Budget Planner":

    st.title("💵 Monthly Budget Planner")

    st.write("Compare your recorded expenses with your planned budget.")

    budget = st.number_input(
        "Enter your monthly budget (₹)",
        min_value=1.0,
        value=30000.0,
        step=1000.0
    )

    if st.button("Analyze Budget"):

        transactions = get_current_data()

        try:

            result = calculate_budget_status(
                transactions,
                budget
            )

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Monthly Budget",
                format_inr(result["monthly_budget"])
            )

            col2.metric(
                "Total Expenses",
                format_inr(result["total_expenses"])
            )

            col3.metric(
                "Remaining Budget",
                format_inr(result["remaining_budget"])
            )

            usage = result["budget_usage"]

            st.progress(min(max(usage / 100, 0.0), 1.0))

            st.write(f"Budget Usage: {usage:.2f}%")

            if result["status"] == "Over Budget":
                st.error("You have exceeded your budget.")
            else:
                st.success("You are within your budget.")

        except Exception as error:

            st.error(str(error))


# --------------------------------------------------
# AI FINANCE ASSISTANT
# --------------------------------------------------

elif page == "AI Finance Assistant":

    st.title("🤖 AI Finance Assistant")

    st.write(
        "Ask questions about your spending, budget and savings."
    )

    st.info(
        "FinGuard uses a local Qwen 2.5 3B model through Ollama."
    )

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input(
        "Ask something about your finances..."
    )

    if question:

        st.session_state.chat_history.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):

            with st.spinner("FinGuard AI is analyzing..."):

                answer = agent.ask_question(question)

                st.markdown(answer)

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer
        })


# --------------------------------------------------
# SAFETY CENTER
# --------------------------------------------------

elif page == "Safety Center":

    st.title("🛡️ AI Safety Center")

    st.write(
        "FinGuard AI uses multiple safety checks to help "
        "protect user inputs and maintain responsible AI responses."
    )

    safety_features = [
        (
            "Input Validation",
            "Checks empty, oversized and suspicious user inputs."
        ),
        (
            "Privacy Protection",
            "Detects and masks certain sensitive information patterns."
        ),
        (
            "Content Validation",
            "Validates transaction data and descriptions."
        ),
        (
            "Output Filtering",
            "Checks AI responses for selected unsafe financial claims."
        ),
        (
            "Local AI Processing",
            "Uses a locally running Ollama model."
        ),
        (
            "Verified Financial Calculations",
            "Uses Python calculations instead of relying on AI arithmetic."
        )
    ]

    for title, description in safety_features:

        with st.container(border=True):

            st.markdown(f"### ✅ {title}")
            st.write(description)

    st.divider()

    st.subheader("Important Disclaimer")

    st.warning(
        "FinGuard AI is an educational personal finance assistant. "
        "It does not connect to bank accounts, make payments, "
        "or provide professional financial or investment advice. "
        "Its safety checks are limited and cannot guarantee "
        "that every unsafe input or output will be detected."
    )

    st.caption(
        "Use synthetic data for academic demonstrations. "
        "Do not enter real banking credentials, PINs or OTPs."
    )
