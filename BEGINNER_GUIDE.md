# How to Create the AI Database Agent Framework - Beginner's Guide

## What You Need to Know First

This framework helps you:
- Create a database automatically
- Use AI (Llama 3) to test your database
- Check if your data is correct
- Create HTML reports of your tests

It's like having a robot that checks your database for problems!

---

## Step 1: Get the Tools Ready

### What to Install (In Order)

#### 1. **Python**
- Go to https://www.python.org/downloads/
- Download Python 3.10 or higher
- When installing, **CHECK the box** "Add Python to PATH"
- Click "Install Now"

**Check if Python is installed:**
```
Open Command Prompt (or PowerShell)
Type: python --version
You should see: Python 3.x.x
```

#### 2. **Git** (for saving your code)
- Go to https://git-scm.com/download/win
- Download and install (default settings are fine)
- Click "Install"

**Check if Git is installed:**
```
Open Command Prompt
Type: git --version
You should see: git version 2.x.x
```

#### 3. **Ollama** (for AI/LLM)
- Go to https://ollama.ai
- Download for Windows
- Install and run it

**Important:** After installing, Ollama needs to download the AI model:
```
Open Command Prompt
Type: ollama pull llama3
Wait 10-15 minutes (it's a 4.7GB download)
```

**Check if Ollama is working:**
```
Open a new Command Prompt
Type: ollama serve
You should see: Listening on 127.0.0.1:11434
Keep this running while you test!
```

---

## Step 2: Create the Folder Structure

Create folders like this (copy exactly):

```
C:\YourWorkspace\
├── Agents\
├── config\
├── database\
├── Tests\
└── reporting\
```

**How to do it:**
```
1. Open File Explorer
2. Create a folder called "YourWorkspace" (any name you like)
3. Inside it, create folders: Agents, config, database, Tests, reporting
```

---

## Step 3: Add the Python Files

### File 1: `config/settings.py`

Copy this code exactly:

```python
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, "database", "bank.db")
```

**Where to save:**
- Save as: `C:\YourWorkspace\config\settings.py`

---

### File 2: `config/__init__.py`

Copy this code exactly:

```python
"""
Configuration module - Settings and environment variables
"""
from .settings import BASE_DIR, DATABASE_PATH

__all__ = ["BASE_DIR", "DATABASE_PATH"]
```

**Where to save:**
- Save as: `C:\YourWorkspace\config\__init__.py`

---

### File 3: `database/__init__.py`

Copy this (it's just a comment file):

```python
"""
Database module - Schema definitions
"""
```

**Where to save:**
- Save as: `C:\YourWorkspace\database\__init__.py`

---

### File 4: `database/schema.py`

This is a big file with table definitions. Here's a simplified version:

```python
import sqlite3
from config import DATABASE_PATH

conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

# Table definitions
tables = {
    "customers": {
        "drop": "DROP TABLE IF EXISTS customers",
        "create": """
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT,
                country TEXT,
                risk_rating TEXT
            )
        """,
        "indexes": [
            "CREATE INDEX IF NOT EXISTS idx_customers_risk ON customers(risk_rating)"
        ],
        "data": [
            (1, "John Miller", "john.miller@email.com", "USA", "Low"),
            (2, "Mary Johnson", "mary.johnson@email.com", "UK", "Medium"),
            (3, "Raj Patel", "raj.patel@email.com", "India", "Low"),
        ],
    },
    "accounts": {
        "drop": "DROP TABLE IF EXISTS accounts",
        "create": """
            CREATE TABLE IF NOT EXISTS accounts (
                account_id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                account_type TEXT,
                balance INTEGER
            )
        """,
        "indexes": [
            "CREATE INDEX IF NOT EXISTS idx_accounts_customer ON accounts(customer_id)"
        ],
        "data": [
            (101, 1, "Savings", 12000),
            (102, 2, "Checking", 8000),
            (103, 3, "Savings", 5000),
        ],
    },
}
```

**Where to save:**
- Save as: `C:\YourWorkspace\database\schema.py`

---

### File 5: `Agents/__init__.py`

```python
"""
Agents module - Database testing and validation agents
"""
```

**Where to save:**
- Save as: `C:\YourWorkspace\Agents\__init__.py`

---

### File 6: `Agents/db_agent.py`

This is the main file that creates your database:

```python
# db_agent.py

import sqlite3
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.schema import tables
from config import DATABASE_PATH

# Connect to database
conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

print("Creating database...")

# Create all tables
for table_name, table_info in tables.items():
    if "drop" in table_info:
        cursor.execute(table_info["drop"])
    
    cursor.execute(table_info["create"])
    
    # Create indexes
    for index in table_info.get("indexes", []):
        cursor.execute(index)
    
    # Insert sample data
    for row in table_info.get("data", []):
        placeholders = ','.join(['?']*len(row))
        cursor.execute(f"INSERT OR REPLACE INTO {table_name} VALUES ({placeholders})", row)

conn.commit()
print("✓ Database created successfully!")

# Show what was created
for table_name in tables.keys():
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    print(f"\nTable: {table_name}")
    print(f"Rows: {len(rows)}")

conn.close()
```

**Where to save:**
- Save as: `C:\YourWorkspace\Agents\db_agent.py`

---

### File 7: `Tests/__init__.py`

```python
"""
Tests module - Testing suites
"""
```

**Where to save:**
- Save as: `C:\YourWorkspace\Tests\__init__.py`

---

### File 8: `Tests/data_quality_tests.py`

```python
"""
Data Quality Tests - Check for bad data
"""

def data_quality_tests(cursor):
    """Check for NULL values, duplicates, and type issues"""
    
    tests = []
    
    # Test 1: Find NULL values
    cursor.execute("SELECT COUNT(*) FROM customers WHERE email IS NULL")
    null_emails = cursor.fetchone()[0]
    tests.append({
        "name": "NULL Email Check",
        "passed": null_emails == 0,
        "result": f"Found {null_emails} NULL emails"
    })
    
    # Test 2: Find duplicates
    cursor.execute("""
        SELECT COUNT(*) FROM (
            SELECT name FROM customers GROUP BY name HAVING COUNT(*) > 1
        )
    """)
    duplicates = cursor.fetchone()[0]
    tests.append({
        "name": "Duplicate Names Check",
        "passed": duplicates == 0,
        "result": f"Found {duplicates} duplicate names"
    })
    
    return tests
```

**Where to save:**
- Save as: `C:\YourWorkspace\Tests\data_quality_tests.py`

---

### File 9: `Tests/etl_tests.py`

```python
"""
ETL Tests - Check data pipeline
"""

def etl_checks(cursor):
    """Check if data moves correctly"""
    
    tests = []
    
    # Test: Count check
    cursor.execute("SELECT COUNT(*) FROM customers")
    customer_count = cursor.fetchone()[0]
    
    tests.append({
        "name": "Customer Count",
        "passed": customer_count > 0,
        "result": f"Total customers: {customer_count}"
    })
    
    return tests
```

**Where to save:**
- Save as: `C:\YourWorkspace\Tests\etl_tests.py`

---

### File 10: `Tests/aml_tests.py`

```python
"""
AML Tests - Check for risky transactions
"""

def aml_checks(cursor):
    """Check for suspicious activity"""
    
    tests = []
    
    # Test: Find high-risk customers
    cursor.execute("""
        SELECT COUNT(*) FROM customers WHERE risk_rating = 'High'
    """)
    high_risk = cursor.fetchone()[0]
    
    tests.append({
        "name": "High Risk Customers",
        "passed": high_risk < 5,
        "result": f"Found {high_risk} high-risk customers"
    })
    
    return tests
```

**Where to save:**
- Save as: `C:\YourWorkspace\Tests\aml_tests.py`

---

### File 11: `reporting/__init__.py`

```python
"""
Reporting module - Generate reports
"""
```

**Where to save:**
- Save as: `C:\YourWorkspace\reporting\__init__.py`

---

### File 12: `reporting/report_generator.py`

```python
"""
Generate HTML reports from test results
"""

def generate_report(results):
    """Create an HTML report"""
    
    html = """
    <html>
    <head>
        <title>Database Test Report</title>
        <style>
            body { font-family: Arial; margin: 20px; }
            .pass { color: green; }
            .fail { color: red; }
        </style>
    </head>
    <body>
        <h1>Database Test Report</h1>
        <table border="1">
            <tr>
                <th>Test Name</th>
                <th>Status</th>
                <th>Details</th>
            </tr>
    """
    
    for result in results:
        status = "✓ PASS" if result.get("passed") else "✗ FAIL"
        html += f"""
            <tr>
                <td>{result.get("name", "Unknown")}</td>
                <td class="{'pass' if result.get('passed') else 'fail'}">{status}</td>
                <td>{result.get("result", "No details")}</td>
            </tr>
        """
    
    html += """
        </table>
    </body>
    </html>
    """
    
    return html
```

**Where to save:**
- Save as: `C:\YourWorkspace\reporting\report_generator.py`

---

## Step 4: Create Important Files

### File 13: `.gitignore`

This tells Git which files NOT to save:

```
__pycache__/
*.py[cod]
*.db
*.sqlite
reporting/Results/*
venv/
.vscode/
```

**Where to save:**
- Save as: `C:\YourWorkspace\.gitignore`

---

### File 14: `requirements.txt`

List of Python packages you need:

```
langchain-community>=0.0.1
ollama>=0.1.0
```

**Where to save:**
- Save as: `C:\YourWorkspace\requirements.txt`

---

### File 15: `README.md`

Instructions for others (or for you later):

```markdown
# AI Database Agent Framework

## Quick Start

1. Install Python and Ollama
2. Run: `python Agents/db_agent.py`
3. Check: `database/bank.db` was created

## What it does

- Creates a test database
- Can test data quality
- Checks for bad data

## Files

- `Agents/db_agent.py` - Creates database
- `Tests/` - Test scripts
- `reporting/` - Report generation
```

**Where to save:**
- Save as: `C:\YourWorkspace\README.md`

---

## Step 5: Install Python Packages

This is needed for the AI features to work.

```
1. Open Command Prompt (or PowerShell)
2. Go to your folder:
   cd C:\YourWorkspace
3. Type:
   pip install -r requirements.txt
4. Wait for it to finish
```

---

## Step 6: Test It Works!

Now run your first database:

```
1. Open Command Prompt
2. Go to your folder:
   cd C:\YourWorkspace
3. Run the database creator:
   python Agents/db_agent.py
4. You should see:
   ✓ Database created successfully!
   Table: customers
   Rows: 3
   Table: accounts
   Rows: 3
```

**Check if database exists:**
```
1. Open File Explorer
2. Go to: C:\YourWorkspace\database\
3. You should see: bank.db
```

---

## Step 7: Save to GitHub (Optional)

If you want to save your code online:

```
1. Go to GitHub.com and create a free account
2. Create a new repository (named "ai-db-agent")
3. Open Command Prompt in your folder:
   cd C:\YourWorkspace
4. Run these commands:
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_NAME/ai-db-agent.git
   git push -u origin master
5. Your code is now online!
```

---

## What Each File Does

| File | Purpose |
|------|---------|
| `config/settings.py` | Store settings (like where database is) |
| `database/schema.py` | Define database tables and sample data |
| `Agents/db_agent.py` | Create the database |
| `Tests/*.py` | Test your data |
| `reporting/report_generator.py` | Create HTML reports |

---

## Running Your Tests

After you create the database, you can run tests:

```python
# Create a file called: run_tests.py

import sqlite3
from config import DATABASE_PATH
from Tests.data_quality_tests import data_quality_tests

# Connect to database
conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

# Run tests
results = data_quality_tests(cursor)

# Show results
for test in results:
    status = "✓ PASS" if test["passed"] else "✗ FAIL"
    print(f"{test['name']}: {status}")
    print(f"  Details: {test['result']}")

conn.close()
```

---

## Common Problems & Solutions

### Problem: "ModuleNotFoundError: No module named 'config'"

**Solution:**
- Make sure you're running from the main folder (C:\YourWorkspace\)
- Make sure `config/__init__.py` exists

### Problem: "Python is not installed"

**Solution:**
- Go to https://www.python.org/downloads/
- Download and install
- IMPORTANT: Check "Add Python to PATH"

### Problem: "Ollama is not running"

**Solution:**
- Open Command Prompt
- Type: `ollama serve`
- Leave it running while you test
- It will say: "Listening on 127.0.0.1:11434"

### Problem: "Database file not created"

**Solution:**
- Check that `database/` folder exists
- Make sure `database/__init__.py` exists
- Run: `python Agents/db_agent.py` from main folder

---

## Next Steps

Once this is working, you can:

1. **Add more data** to `database/schema.py`
2. **Create more tests** in the `Tests/` folder
3. **Add AI features** using Ollama
4. **Generate fancy reports** from test results

---

## Getting Help

If something doesn't work:

1. **Read the error message** - it tells you what's wrong
2. **Check file paths** - make sure files are in the right place
3. **Check file names** - Python is picky about spelling
4. **Search online** - copy the error message into Google

---

## Congratulations!

You've created a database testing framework! 🎉

Now you have:
- ✓ A database that creates itself
- ✓ Tests that check your data
- ✓ Reports that show results

Keep building! 🚀
