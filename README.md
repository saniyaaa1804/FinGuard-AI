# 💰 FinGuard AI – Personal Finance Assistant

**An AI-powered personal finance assistant for smarter budgeting, expense tracking, and financial awareness.**

## 📌 Project Overview

FinGuard AI is an AI-powered personal finance assistant designed to help users understand their income, monitor expenses, manage monthly budgets, and receive personalized savings suggestions.

The application combines Python-based financial calculations, a SQLite database, and a locally running Large Language Model (LLM) through Ollama to provide interactive financial insights.

It also incorporates multiple AI safety mechanisms to validate user inputs, detect sensitive information, validate transaction data, and filter potentially unsafe AI responses.

## 🎯 Project Objectives

- Track income and expenses efficiently.
- Analyze spending patterns across different categories.
- Calculate remaining balance and savings rate.
- Help users plan and monitor monthly budgets.
- Provide AI-powered financial explanations and savings suggestions.
- Implement responsible AI practices and privacy protection.
- Perform AI inference locally using Ollama.

## ✨ Key Features

### 1. Financial Dashboard
- Displays total income and expenses.
- Shows remaining balance and savings rate.
- Visualizes expense distribution using interactive charts.
- Displays recent financial transactions.
- Provides rule-based savings suggestions.

### 2. Transaction Management
- Add income and expense transactions.
- Select transaction dates and categories.
- Store financial records in SQLite.
- View previously recorded transactions.

### 3. Monthly Budget Planner
- Set a monthly spending budget.
- Calculate total recorded expenses.
- Display remaining budget.
- Monitor budget utilization.
- Identify when spending exceeds the planned budget.

### 4. AI Finance Assistant
- Interactive AI-powered financial chatbot.
- Answers questions about budgeting and spending.
- Provides general savings suggestions.
- Explains financial summaries in natural language.
- Uses a locally running Qwen 2.5 3B model through Ollama.

### 5. AI Safety Center
- Input validation and prompt injection detection.
- Sensitive information detection and masking.
- Transaction content validation.
- AI output filtering.
- Local AI processing.
- Python-based financial calculations for numerical accuracy.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.13 | Core programming language |
| Streamlit | Web application interface |
| SQLite | Database management |
| Ollama | Local LLM execution |
| Qwen 2.5 3B | AI finance assistant |
| LangChain | LLM integration |
| Plotly Graph Objects | Interactive visualizations |
| CSV | Sample transaction dataset |

**Additional implementation:** Python built-in modules such as `csv`, `sqlite3`, `re`, and `pathlib`.

## 🏗️ Project Architecture

```text
FinGuard-AI/
│
├── app.py
├── agent.py
├── database.py
├── finance_tools.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── guards/
│   ├── __init__.py
│   ├── input_guard.py
│   ├── privacy_guard.py
│   ├── content_guard.py
│   └── output_guard.py
│
├── utils/
│   ├── __init__.py
│   ├── prompts.py
│   └── calculations.py
│
├── data/
│   └── sample_transactions.csv
│
└── logs/
    └── activity.log
```

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.13
- Ollama
- Git (optional)

### Step 1: Clone the repository

```bash
git clone https://github.com/omakolkar4/FinGuard-AI.git
```

```bash
cd FinGuard-AI
```

### Step 2: Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### Step 3: Install dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 4: Download the AI model

Make sure Ollama is installed and running.

```bash
ollama pull qwen2.5:3b
```

Verify the model:

```bash
ollama list
```

### Step 5: Run the application

```bash
python -m streamlit run app.py
```

Open the application in your browser:

```text
http://localhost:8501
```

## 📊 Sample Financial Analysis

The application includes a sample dataset containing 15 financial transactions.

| Financial Metric | Amount |
|---|---:|
| Total Income | ₹50,000 |
| Total Expenses | ₹28,099 |
| Remaining Balance | ₹21,901 |
| Savings Rate | 43.8% |

*These figures are based on the included sample transaction dataset.*

## 🔐 Responsible AI and Safety

FinGuard AI incorporates multiple safety layers:

1. **Input Guard:** Detects empty, oversized, and selected suspicious inputs.
2. **Privacy Guard:** Identifies and masks certain sensitive information patterns.
3. **Content Guard:** Validates transaction descriptions and financial data.
4. **Output Guard:** Filters selected unsafe financial claims in AI-generated responses.

The application uses local AI inference through Ollama, helping avoid sending user questions to a hosted LLM API.

Python performs the financial calculations, while the AI model explains the results.

## 🧠 AI Workflow

```text
       User Input
            |
            v
      Input Validation
            |
            v
      Privacy Protection
            |
            v
   Financial Data Retrieval
            |
            v
   Python Financial Analysis
            |
            v
      Qwen 2.5 3B Model
            |
            v
      Output Validation
            |
            v
      Final AI Response
```

## 🚀 Future Enhancements

- Monthly and yearly financial reports.
- Advanced spending trend analysis.
- Export financial reports to PDF and CSV.
- Goal-based savings planner.
- Multi-user authentication.
- Enhanced AI-based financial insights.
- More comprehensive prompt injection and privacy protection.

## ⚠️ Disclaimer

FinGuard AI is an educational personal finance assistant developed for academic and demonstration purposes.

It does not connect to real bank accounts, perform financial transactions, or provide professional financial or investment advice.

The safety mechanisms provide limited protection and cannot guarantee detection of every unsafe input or output.

Use synthetic financial data for demonstrations. Never enter banking passwords, PINs, OTPs, or card credentials.

## 👨‍💻 Project Information

**Project Name:** FinGuard AI – Personal Finance Assistant

**Domain:** Agentic AI / Artificial Intelligence

**Application Type:** Web-Based Application

**AI Model:** Qwen 2.5 3B

**Backend:** Python

**Database:** SQLite

**Interface:** Streamlit

---

**Developed as an academic project to demonstrate AI-powered personal finance assistance, financial data analysis, local LLM integration, and responsible AI practices.**