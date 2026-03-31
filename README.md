# AI Database Agent Platform

## Project Structure

```
ai-db-agent-demo/
├── Agents/
│   ├── __init__.py
│   ├── db_agent.py              # Database initialization
│   └── enterprise_ai_db_agent.py # AI-powered testing agent
├── database/
│   ├── __init__.py
│   ├── schema.py                # Table definitions & sample data
│   └── bank.db                  # SQLite database (created at runtime)
├── config/
│   ├── __init__.py
│   └── settings.py              # Configuration settings
├── Tests/
│   ├── __init__.py
│   ├── data_quality_tests.py    # Data quality validation
│   ├── etl_tests.py             # ETL pipeline testing
│   └── aml_tests.py             # AML compliance testing
├── reporting/
│   ├── __init__.py
│   ├── report_generator.py      # HTML report generation
│   └── Results/                 # Generated reports (output folder)
├── PRESENTATION.md              # Demo presentation
└── README.md                    # This file
```

## Installation

### Prerequisites
- Python 3.8+
- Ollama (for LLM execution)
- SQLite3 (usually pre-installed)

### Setup

```bash
# 1. Install Python dependencies
pip install langchain-community
pip install ollama

# 2. Pull Llama 3 model (one-time setup)
ollama pull llama3

# 3. Verify Ollama is running
# On a separate terminal:
ollama serve
```

## Usage

### 1. Initialize Database

```bash
cd Agents
python db_agent.py
```

This creates:
- `database/bank.db` with 5 tables
- Sample banking data (customers, accounts, transactions)
- Compliance alerts for testing

### 2. Run AI Testing Agent

```bash
python enterprise_ai_db_agent.py
```

This performs:
- Automatic database schema discovery
- AI-powered test generation (via Llama 3)
- Safe SQL query validation
- Comprehensive testing across:
  - Data quality (NULLs, duplicates, constraints)
  - ETL validation (source→target reconciliation)
  - AML compliance (risk detection)

### 3. Generate HTML Report

```bash
cd ../reporting
python report_generator.py
```

Output: `Results/db_test_report.html`

## Features

### Database Testing
- ✅ Automatic schema introspection
- ✅ AI-generated test queries
- ✅ Safe SQL validation (prevents DROP/DELETE/UPDATE)
- ✅ PII data masking in reports

### Compliance
- ✅ AML (Anti-Money Laundering) detection
- ✅ Risk assessment and scoring
- ✅ Regulatory-compliant reporting

### Data Quality
- ✅ NULL value detection
- ✅ Duplicate identification
- ✅ Type validation
- ✅ Referential integrity checks

## Configuration

Edit `config/settings.py` to customize:
- Database location
- LLM model selection
- Test parameters

## Architecture

```
┌─────────────────────────────────────────┐
│     Database Agent (db_agent.py)        │
│  ├─ SQLite initialization               │
│  ├─ Schema creation                     │
│  └─ Sample data loading                 │
└─────────────┬───────────────────────────┘
              ▼
┌─────────────────────────────────────────┐
│   Enterprise AI Agent                   │
│  ├─ Schema discovery (PRAGMA)           │
│  ├─ Test generation (Llama 3)          │
│  ├─ Query validation                    │
│  └─ Test execution                      │
└─────────────┬───────────────────────────┘
              ▼
┌─────────────────────────────────────────┐
│     Testing Framework                   │
│  ├─ Data Quality Tests                  │
│  ├─ ETL Tests                           │
│  └─ AML Compliance Tests                │
└─────────────┬───────────────────────────┘
              ▼
┌─────────────────────────────────────────┐
│     Report Generation                   │
│  └─ HTML reports with metrics           │
└─────────────────────────────────────────┘
```

## Security

- **Safe SQL Execution**: Only SELECT and PRAGMA queries are allowed
- **PII Protection**: Customer names and emails are masked in reports
- **Query Validation**: Dangerous operations (DROP, DELETE, UPDATE) are blocked
- **Local Processing**: All operations run locally via Ollama

## Troubleshooting

### ModuleNotFoundError
- Ensure you're in the `Agents/` directory or run from project root
- Python path is automatically configured for imports

### Ollama not found
- Ensure Ollama is installed: `ollama --version`
- Start Ollama server in another terminal: `ollama serve`

### Database path issues
- Database is stored at: `database/bank.db`
- Configured in `config/settings.py`

## Demo

See `PRESENTATION.md` for a full presentation guide with:
- Architecture overview
- Step-by-step demo script
- Key talking points
- Q&A section

## License

This project is for demonstration and educational purposes.
