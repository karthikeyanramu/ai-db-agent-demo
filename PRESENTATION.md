# AI Database Agent Platform
## Comprehensive Technical Demonstration

---

# 🎯 Executive Summary

**An intelligent Python-based application that combines:**
- 🤖 AI-powered database intelligence (Llama 3 + Ollama)
- 🔒 Secure multi-layer system architecture
- 🗄️ SQLite-based persistent banking data storage
- 🔧 Advanced testing & compliance automation
- 📊 Enterprise-grade reporting and analytics

**Use Case:** Automated database validation, data quality testing, AML compliance checking, and intelligent SQL query generation with local LLM integration

---

# 📋 Agenda

1. **Architecture Overview** - High-level system design
2. **Python Backend Services** - LangChain, Ollama, Llama 3
3. **Database Services** - SQLite, Banking Schema
4. **Testing & Validation Framework** - Data Quality, ETL, AML
5. **Reporting Engine** - HTML report generation
6. **Compliance & Security** - Safe SQL execution, data masking

---

# 🏗️ Architecture Overview

## System Design

```
┌─────────────────────────────────────────────────────────┐
│           PYTHON AGENT LAYER (Backend)                  │
│  LangChain + Ollama + Llama 3 + SQLite                 │
└────────────┬────────────────────────────────────┬───────┘
             │                                    │
             ▼                                    ▼
    ┌──────────────────┐            ┌──────────────────────┐
    │  DB Agent        │            │  Reporting Engine    │
    │  - Schema Intro  │            │  - HTML Report Gen   │
    │  - Safe SQL Exec │            │  - Metrics & Stats   │
    └────────┬─────────┘            └──────────┬───────────┘
             │                                  │
             └──────────────┬───────────────────┘
                            ▼
            ┌──────────────────────────────┐
            │   Validation Framework       │
            │  - Data Quality Tests        │
            │  - ETL Tests                 │
            │  - AML Compliance Tests      │
            └──────────────┬───────────────┘
                           │
                           ▼
            ┌────────────────────────────┐
            │   SQLite Database          │
            │  (bank.db)                 │
            │  - Customers               │
            │  - Accounts                │
            │  - Transactions            │
            └────────────────────────────┘
```

---

# 🐍 Python Backend Stack

## Core Technologies

| Technology | Component | Purpose |
|-----------|-----------|----------|
| **Python 3** | Language | Core backend implementation |
| **LangChain** | Agent Framework | Orchestrating LLM-based workflows |
| **Ollama** | LLM Runtime | Local execution engine |
| **Llama 3** | Language Model | 7B parameter open-source LLM |
| **SQLite3** | Database | Persistent banking data storage |
| **Jinja2** | Templating | HTML report generation |

---

## Core Services

### 1️⃣ **Database Agent**
**Location:** [`Agents/db_agent.py`](Agents/db_agent.py)

**Responsibilities:**
- ✅ SQLite3 database connection and initialization
- ✅ Table schema creation with banking domain data
- ✅ Index creation for query optimization
- ✅ Sample data population (customers, accounts, transactions)
- ✅ Masked customer view creation for PII protection
- ✅ ETL simulation (raw → transformed data)

**Key Functions:**
```python
conn = sqlite3.connect("bank.db")  # Initialize DB
cursor.execute(table_schema)        # Create tables
cursor.execute(create_index)        # Create indexes
insert_sample_data()                # Populate data
```

**Database Objects:**
- **customers** table: customer_id, name, email, country, risk_rating
- **accounts** table: account_id, customer_id, account_type, balance
- **transactions** table: transaction_id, account_number, amount, date
- **masked_customers** view: PII-redacted customer data

---

### 2️⃣ **Enterprise AI Database Agent**
**Location:** [`Agents/enterprise_ai_db_agent.py`](Agents/enterprise_ai_db_agent.py)

**Responsibilities:**
- 🤖 LLM-powered test generation using Llama 3
- 🔍 Automatic database schema discovery via PRAGMA
- 🛡️ Safe SQL query validation and execution
- 📊 Multi-format test result handling
- 🔧 Integration with testing suite

**Key Capabilities:**
```python
schema = discover_schema(cursor)        # Introspect database
tests = generate_ai_tests(schema, llm)  # Generate via LLM
is_safe = is_safe_query(query)         # Validate safety
execute_tests(cursor, tests)           # Run safely
```

**LLM Configuration:**
- Model: Llama 3 (7B parameters)
- Runtime: Ollama (local execution)
- Integration: LangChain Community

---
# � Project Directory Structure

## Current Workspace Layout

```
ai-db-agent-demo/
├── Agents/
│   ├── db_agent.py
│   │   └── Database initialization and setup
│   ├── enterprise_ai_db_agent.py
│   │   └── LLM-powered testing and validation
│   └── bank.db
│       └── SQLite database (runtime created)
├── database/
│   └── schema.py
│       └── Schema definitions and sample data
├── config/
│   └── settings.py
│       └── Configuration management
├── Tests/
│   ├── data_quality_tests.py
│   ├── etl_tests.py
│   └── aml_tests.py
├── reporting/
│   ├── report_generator.py
│   └── Results/
│       └── db_test_report.html (generated reports)
├── PRESENTATION.md (this file)
└── .github/
    └── copilot-instructions.md (coding guidelines)
```

---

## 1️⃣ Database Agent (`db_agent.py`)

### Initialization Pipeline

```python
1. Connect to SQLite ("bank.db")
   
2. CREATE TABLES
   ├── customers (customer_id, name, email, country, risk_rating)
   ├── accounts (account_id, customer_id, account_type, balance)
   ├── transactions (transaction_id, account_number, amount, date)
   └── raw_transactions (source data for ETL)

3. CREATE INDEXES
   ├── idx_customers_risk (risk_rating)
   └── idx_accounts_customer (customer_id)

4. INSERT SAMPLE DATA
   ├── 10 customer records (global diversity)
   ├── 12+ account records (varied balances)
   └── Transaction records

5. CREATE MASKED VIEW
   └── masked_customers (PII redaction: name, email)

6. SIMULATE ETL
   └── Transform raw_transactions → transactions table
```

### Sample Data Preview

**Customers Table:**
| customer_id | name | email | country | risk_rating |
|---|---|---|---|---|
| 1 | John Miller | john.miller@email.com | USA | Low |
| 2 | Mary Johnson | mary.johnson@email.com | UK | Medium |
| 11 | Raj Patel | raj.patel2@email.com | UAE | High |
| ... | ... | ... | ... | ... |

**Accounts Table:**
| account_id | customer_id | account_type | balance |
|---|---|---|---|
| 101 | 1 | Savings | 12,000 |
| 102 | 2 | Checking | 8,000 |
| 104 | 4 | Checking | 250,000 |

---

## 2️⃣ Enterprise AI Agent (`enterprise_ai_db_agent.py`)

### Technology Stack

```
┌──────────────────────────────────────────┐
│     langchain_community.llms.Ollama       │
│      (Local LLM execution engine)         │
└────────────────────┬─────────────────────┘
                     ▼
        ┌────────────────────┐
        │   Llama 3 Model    │
        │  (7B parameters)   │
        └────────────────────┘
```

### Core Functions

#### **1. Schema Discovery**
```python
def discover_schema(cursor):
    """Introspect database structure"""
    ├─ Fetch all table names
    ├─ Extract column definitions
    ├─ Build schema dictionary
    └─ Return: {table_name: [columns]}
```

#### **2. AI SQL Generation**
```python
def generate_ai_tests(schema, llm):
    """Generate test queries using Llama 3"""
    ├─ Build prompt with schema
    ├─ Call local Ollama LLM
    ├─ Clean SQL output
    └─ Return: List of test queries
```

#### **3. Safe Query Validation**
```python
def is_safe_query(query):
    """Prevent destructive operations"""
    ├─ Whitelist: SELECT, CREATE (SELECT), PRAGMA
    └─ Blacklist: DROP, DELETE, UPDATE, INSERT, ALTER
```

#### **4. SQL Execution & Results**
```python
def execute_tests(cursor, queries):
    """Run validation queries safely"""
    ├─ Validate each query
    ├─ Execute if safe
    ├─ Capture results & metrics
    └─ Handle errors gracefully
```

### Testing Workflows

#### **Data Quality Tests**
- Missing value detection
- Duplicate record identification
- Data type validation
- Range/constraint checks

#### **ETL Tests**
- Source → Target record counts
- Data transformation accuracy
- Timestamp consistency
- Key relationship integrity

#### **AML Tests** (Anti-Money Laundering)
- High-risk customer flagging
- Transaction pattern anomalies
- Geographic risk assessment
- Threshold violation detection

---

## 3️⃣ Report Generation

**Location:** [`reporting/report_generator.py`](reporting/report_generator.py)

### Output Format

```
HTML Report Structure
├─ Test Execution Summary
│  ├─ Total tests run
│  ├─ Pass/Fail counts
│  └─ Execution timestamp
├─ Detailed Test Results
│  ├─ Test name & description
│  ├─ SQL query executed
│  ├─ Result rows
│  └─ Status indicator
├─ Data Quality Metrics
│  └─ Charts & statistics
└─ Compliance Summary
   └─ Risk assessment results
```

**Example Report:** [Results/db_test_report.html](Results/db_test_report.html)

---

# 🗄️ Data Layer (SQLite3)

## Banking Domain Schema

### Customers Table

```sql
CREATE TABLE customers (
  customer_id INTEGER PRIMARY KEY,
  name TEXT,
  email TEXT,
  country TEXT,
  risk_rating TEXT  -- 'Low', 'Medium', 'High'
)
```

**Indexes:**
- `idx_customers_risk` on risk_rating (for compliance queries)

**Sample Data:**
| ID | Name | Email | Country | Risk |
|----|------|-------|---------|---------|
| 1 | John Miller | john.miller@email.com | USA | Low |
| 2 | Mary Johnson | mary.johnson@email.com | UK | Medium |
| 11 | Raj Patel | raj.patel2@email.com | UAE | High |

### Accounts Table

```sql
CREATE TABLE accounts (
  account_id INTEGER PRIMARY KEY,
  customer_id INTEGER,
  account_type TEXT,  -- 'Savings', 'Checking'
  balance INTEGER
)
```

**Indexes:**
- `idx_accounts_customer` on customer_id (for joins)

### Transactions Table

```sql
CREATE TABLE transactions (
  transaction_id INTEGER PRIMARY KEY,
  account_number INTEGER,
  amount REAL,
  txn_date TEXT
)
```

### Data Protection: Masked Views

```sql
CREATE VIEW masked_customers AS
SELECT
  customer_id,
  SUBSTR(name,1,1) || '***' AS name,
  SUBSTR(email,1,2) || '***@***.com' AS email,
  risk_rating
FROM customers
```

**Purpose:** PII (Personally Identifiable Information) redaction for secure reporting

---

# 🔒 Security & Data Protection

## Safe SQL Execution

### Query Validation Pipeline

```python
def is_safe_query(query):
    """Prevent malicious SQL operations"""
    
    dangerous = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER"]
    
    for word in dangerous:
        if word in query.upper():
            return False
    
    return True  # Safe for execution
```

**Whitelist:** SELECT, CREATE (SELECT), PRAGMA
**Blacklist:** DROP, DELETE, UPDATE, INSERT, ALTER

**Purpose:** Protect against:
- Accidental data destruction
- Malicious SQL injection
- Unauthorized data modification

### Execution Flow

```
1. Clean SQL Output
   └─ Remove markdown code blocks
   
2. Validate Query
   └─ Check for dangerous keywords
   
3. Execute If Safe
   └─ Read-only dictionary scan
   
4. Capture Results
   └─ Store metrics and rows
   
5. Handle Errors
   └─ Graceful failure with logging
```

## PII Protection

### Data Masking Strategy

**Customer Names:** First letter + ***
- `John Miller` → `J***`

**Email Addresses:** First 2 chars + ***@***.com
- `john.miller@email.com` → `jo***@***.com`

**Risk Rating:** Fully visible (needed for compliance)

### Masked View Usage

```sql
SELECT * FROM masked_customers
-- Safe for reporting without PII exposure
```

## Configuration Management

**Location:** [`config/settings.py`](config/settings.py)

```python
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, "database", "bank.db")
```

**Environment Variables (if extended):**
- OLLAMA_URL - Ollama server endpoint
- LLAMA_MODEL - Model name (default: llama3)
- LOG_LEVEL - Logging verbosity

---

# 🚀 Running the Application

## Python Environment Setup

### Prerequisites
- Python 3.8+
- Ollama (for LLM execution)
- SQLite3 (usually pre-installed)

### Install Dependencies

```bash
# Core dependencies
pip install langchain-community
pip install ollama
pip install sqlite3  # usually pre-installed

# For reporting
pip install jinja2
```

### Pull LLM Model

```bash
# Download Llama 3 model (~4.7GB)
ollama pull llama3

# Verify Ollama is running
ollama serve  # or check if already running
```

## Running the Agents

### 1. Initialize Database

```bash
cd Agents
python db_agent.py
# Output: Creates bank.db with tables and sample data
```

### 2. Run Testing Agent

```bash
python enterprise_ai_db_agent.py
# Output: Performs schema discovery, generates tests, validates data
```

### 3. Generate Report

```bash
cd ../reporting
python report_generator.py
# Output: results/db_test_report.html
```

## Execution Flow

```
1. db_agent.py
   └─ Creates bank.db
      ├─ 4 tables
      ├─ Sample data (customers, accounts)
      └─ Masked views

2. enterprise_ai_db_agent.py
   └─ Connects to bank.db
      ├─ Discovers schema via PRAGMA
      ├─ Generates tests via Llama 3
      ├─ Validates queries for safety
      ├─ Executes tests
      └─ Collects results

3. report_generator.py
   └─ Compiles results
      ├─ Creates HTML report
      ├─ Includes metrics
      └─ Saves to reporting/Results/
```

---

# 📊 Key Features & Capabilities

## Data Quality Validation
- ✅ Missing value detection
- ✅ Duplicate record identification
- ✅ Data type validation
- ✅ Range and constraint checks
- ✅ Referential integrity verification

## ETL Pipeline Testing
- ✅ Source → target record count matching
- ✅ Data transformation verification
- ✅ Timestamp consistency validation
- ✅ Key relationship integrity checks
- ✅ Load verification

## AML Compliance Testing
- ✅ High-risk customer identification
- ✅ Transaction pattern anomaly detection
- ✅ Geographic risk assessment
- ✅ Threshold violation alerting
- ✅ Compliance rule enforcement

## System Capabilities
- ✅ Automatic schema discovery
- ✅ AI-powered test generation (Llama 3)
- ✅ Safe SQL query execution
- ✅ PII-protected reporting
- ✅ HTML compliance reports

---

# 🎤 Demo Walkthrough Script

## Demo Script

## Part A: System Overview (2-3 minutes)

### 1. Architecture
> *"Welcome! This is the AI Database Agent Platform. It's a Python-based system for intelligent database testing."*

- Point to: System architecture diagram
- Explain: Three main components
  1. Database Agent (initialization)
  2. Testing Engine (LLM-powered validation)
  3. Reporting (HTML results)

### 2. Technology Stack
> *"We're using modern, open-source technologies..."*

- **LangChain:** Orchestrating LLM workflows
- **Ollama:** Running Llama 3 locally (no cloud costs)
- **SQLite:** Lightweight persistent storage
- **Python:** Core backend language

---

## Part B: Live Demo - Database Initialization (3-4 minutes)

### 1. Database Initialization
> *"First, we initialize the database with banking domain data..."*

```bash
cd Agents
python db_agent.py
```

**What happens:**
1. Creates `bank.db` (SQLite database)
2. Creates 4 tables:
   - customers (10 records, global diversity)
   - accounts (12+ records, varied balances)
   - transactions (multi-step)
   - raw_transactions (ETL source)
3. Creates indexes for performance (risk_rating, customer_id)
4. Creates masked_customers view (PII redaction)

**Show:** The created tables and sample data

---

## Part C: AI Testing Engine (4-5 minutes)

### 2. Run Enterprise AI Agent
> *"Now the interesting part - we let an AI test the database..."*

```bash
python enterprise_ai_db_agent.py
```

**What happens:**

**Step 1: Schema Discovery**
- Connects to bank.db
- Uses PRAGMA table_info() to introspect
- Builds schema dictionary
- Show: Discovered tables and columns

**Step 2: AI Test Generation**
- Sends schema to Llama 3 via Ollama
- LLM generates SQL test queries
- Example output:
  ```sql
  SELECT COUNT(*) FROM customers WHERE email IS NULL
  SELECT customer_id, COUNT(*) FROM accounts GROUP BY customer_id HAVING COUNT(*) > 1
  SELECT * FROM customers WHERE risk_rating NOT IN ('Low', 'Medium', 'High')
  ```

**Step 3: Safety Validation**
- Checks each query for dangerous keywords
- Only SELECT and PRAGMA allowed
- Blocks: DROP, DELETE, UPDATE, INSERT, ALTER
- Show: Validation pass/fail logic

**Step 4: Execution**
- Runs validated queries
- Captures results
- Calculates metrics
- Stores in results object

**Output:** Console displays test results

---

## Part D: Test Suites (2-3 minutes)

### 3. Data Quality Tests
> *"Let's look at the different types of tests..."*

Show: [`Tests/data_quality_tests.py`](Tests/data_quality_tests.py)

**Tests included:**
- ✅ NULL value detection
- ✅ Duplicate identification
- ✅ Type validation
- ✅ Range checking
- ✅ Referential integrity

### 4. ETL Tests
Show: [`Tests/etl_tests.py`](Tests/etl_tests.py)

**Tests included:**
- ✅ Row count matching (raw → target)
- ✅ Data transformation verification
- ✅ Timestamp consistency
- ✅ Relationship integrity

### 5. AML Compliance Tests
Show: [`Tests/aml_tests.py`](Tests/aml_tests.py)

**Tests included:**
- ✅ High-risk customer detection
- ✅ Transaction anomalies
- ✅ Geographic risk scoring
- ✅ Threshold violations

---

## Part E: Reporting (2-3 minutes)

### 6. HTML Report Generation
> *"Finally, we compile everything into an HTML report..."*

```bash
cd ../reporting
python report_generator.py
```

Open: `Results/db_test_report.html`

**Report includes:**
- 📊 Test execution summary (total, pass, fail)
- 📋 Detailed test results with query output
- 📈 Data quality metrics and statistics
- ✓ Compliance status indicators
- 📅 Execution timestamp

---

# 🔑 Key Talking Points

## Architecture & Design
✅ **Modular Python design:** Separate agents for DB, testing, reporting  
✅ **AI-powered automation:** Llama 3 generates and validates tests  
✅ **Open-source stack:** No vendor lock-in (Ollama, LangChain)  
✅ **Local execution:** Privacy-first (Ollama runs on your machine)  

## Security & Compliance
✅ **Safe SQL execution:** Query whitelisting prevents injection attacks  
✅ **PII protection:** Automatic data masking in views  
✅ **Validated operations:** No destructive commands allowed  
✅ **Audit trail:** All test results timestamped and logged  

## Financial Compliance
✅ **AML testing:** Automated money-laundering risk detection  
✅ **Risk scoring:** Geographic and customer-level assessment  
✅ **Compliance reporting:** HTML reports for regulatory review  
✅ **ETL validation:** Source-to-target reconciliation  

## Data Quality
✅ **Comprehensive checks:** NULL detection, duplicates, type validation  
✅ **Referential integrity:** Foreign key relationship testing  
✅ **Anomaly detection:** Pattern-based validation  
✅ **Actionable results:** Clear pass/fail with metrics  

---

# 📚 Repository Navigation

## Quick Reference

**Core Agents:**
- 📍 [`Agents/db_agent.py`](Agents/db_agent.py) - Database initialization
- 📍 [`Agents/enterprise_ai_db_agent.py`](Agents/enterprise_ai_db_agent.py) - AI testing engine
- 📍 [`Agents/bank.db`](Agents/bank.db) - SQLite database (runtime created)

**Schema & Configuration:**
- 📍 [`database/schema.py`](database/schema.py) - Table definitions & sample data
- 📍 [`config/settings.py`](config/settings.py) - Settings management

**Testing Framework:**
- 📍 [`Tests/data_quality_tests.py`](Tests/data_quality_tests.py) - Data quality validation
- 📍 [`Tests/etl_tests.py`](Tests/etl_tests.py) - ETL pipeline verification
- 📍 [`Tests/aml_tests.py`](Tests/aml_tests.py) - Compliance testing

**Reporting:**
- 📍 [`reporting/report_generator.py`](reporting/report_generator.py) - Report generation
- 📍 [`reporting/Results/`](reporting/Results/) - Generated HTML reports

**Project:**
- 📍 [`PRESENTATION.md`](PRESENTATION.md) - This presentation
- 📍 [`.github/copilot-instructions.md`](.github/copilot-instructions.md) - Coding guidelines

---

# ❓ Q&A Section

**Common Questions:**

Q: *Can the AI agent modify the actual database?*
A: **No.** The `is_safe_query()` function prevents DROP, DELETE, UPDATE, INSERT, ALTER operations. The system only executes SELECT and PRAGMA (read-only) queries.

Q: *What happens if Ollama (Llama 3) isn't available?*
A: The enterprise agent will fail with a connection error. Backend requires local Ollama running on port 11434 (default).

Q: *How does data masking work?*
A: A dedicated SQL view (`masked_customers`) redacts PII: names become `J***`, emails become `jo***@***.com`. Risk ratings remain visible for compliance.

Q: *How long does a test run take?*
A: Typically 2-5 minutes depending on database size. Schema discovery is instant, LLM generation varies by model size, execution is fast.

Q: *Can I customize which tests run?*
A: Yes. Each test file (data_quality_tests.py, etl_tests.py, aml_tests.py) is modular and can be edited independently.

Q: *What's the database size limit?*
A: SQLite is suitable for databases up to several GB. For production databases > 10GB, consider PostgreSQL or similar.

Q: *Are test results automatically saved?*
A: Yes. Results are captured in memory and can be persisted via `report_generator.py` to HTML files in the Results folder.

Q: *Can multiple users run tests simultaneously?*
A: The current design is single-user. SQLite has write-locking; multiple concurrent writes could cause issues. Consider PostgreSQL for multi-user scenarios.

---

# 🎬 Closing

**Thank you for exploring the AI Database Agent Platform!**

## Key Takeaways

- 🤖 **Intelligent Automation:** LLM-generated tests adapt to your schema
- 🔒 **Enterprise Security:** Whitelisted queries, data masking, compliance-ready
- 💰 **Cost-Effective:** Open-source stack, local execution, no per-query fees
- 📊 **Complete Visibility:** Comprehensive testing across data quality, ETL, compliance
- ⚡ **Fast Iteration:** Run full test suite in minutes

## Extensibility

The platform is built for customization:
- Add new test types to Tests/ folder
- Extend schema with more banking entities
- Modify LLM prompts for domain-specific tests
- Enhance report templates with custom metrics

---

## Next Steps

1. **Install Ollama:** `ollama pull llama3`
2. **Run demo:** `python Agents/db_agent.py`
3. **Start testing:** `python Agents/enterprise_ai_db_agent.py`
4. **View results:** Open `reporting/Results/db_test_report.html`

---

## Contact & Support

**Questions? Comments? Let's discuss!**

*The complete system is ready for live demonstration. Let's explore it together!*
