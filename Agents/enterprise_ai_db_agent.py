import os
import sys
import sqlite3

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_community.llms import Ollama
from config import DATABASE_PATH
from reporting.report_generator import generate_report

from Tests.data_quality_tests import data_quality_tests
from Tests.etl_tests import etl_checks
from Tests.aml_tests import aml_checks


print("====================================")
print("Enterprise AI Database Testing Agent")
print("====================================")


# -------------------------------
# CONNECT DATABASE
# -------------------------------
try:
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    print("Database connected successfully")
except Exception as e:
    print("Database connection failed:", e)
    sys.exit()


# Load AI model
llm = Ollama(model="llama3")

results = []


# =====================================================
# CLEAN AI SQL OUTPUT
# =====================================================
def clean_sql(ai_response):

    cleaned = ai_response.replace("```sql", "")
    cleaned = cleaned.replace("```", "")
    cleaned = cleaned.strip()

    return cleaned


# =====================================================
# VALIDATE SAFE SQL
# =====================================================
def is_safe_query(query):

    dangerous = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER"]

    for word in dangerous:
        if word in query.upper():
            return False

    return True


# =====================================================
# SCHEMA DISCOVERY
# =====================================================
def discover_schema(cursor):

    schema_info = {}

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    for table in tables:

        table_name = table[0]

        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()

        schema_info[table_name] = [col[1] for col in columns]

    return schema_info


# =====================================================
# AI TEST GENERATOR
# =====================================================
def generate_ai_tests(schema, llm):

    prompt = f"""
You are a database QA engineer.

Generate SQL queries to detect data quality issues.

Schema:
{schema}

Create SQL tests for:
- Null values
- Duplicate records
- Negative amounts
- Future dates
- Invalid balances

Return ONLY raw SQL queries separated by semicolons.
Do NOT include markdown or explanations.
"""

    response = llm.invoke(prompt)

    return response


# =====================================================
# EXECUTE AI TESTS
# =====================================================
def execute_ai_tests(cursor, ai_tests):

    ai_results = []

    queries = ai_tests.split(";")

    for query in queries:

        query = query.strip()

        if not query:
            continue

        if not is_safe_query(query):
            print("Blocked unsafe query:", query)
            continue

        print("\nRunning AI Test:", query)

        try:

            cursor.execute(query)
            rows = cursor.fetchall()

            if rows:
                print("AI Issue detected:", rows)

                ai_results.append(
                    ("AI Generated Test", "FAILED", str(rows), "AI detected issue")
                )

            else:

                ai_results.append(
                    ("AI Generated Test", "PASSED", "No issue found", "")
                )

        except Exception as e:

            print("Query failed:", e)

    return ai_results


# =====================================================
# DISCOVER DATABASE
# =====================================================
print("\nDiscovering Database Schema...")

schema = discover_schema(cursor)

for table, columns in schema.items():
    print(f"Table Found: {table} -> {columns}")


# =====================================================
# TEST SELECTION MENU
# =====================================================
print("\n====================================")
print("Select Tests to Execute")
print("====================================")

print("1 - Data Quality Tests")
print("2 - ETL Tests")
print("3 - AML Tests")
print("4 - AI Generated Tests")
print("5 - Run All Tests")

choices = input(
    "\nEnter test numbers separated by comma (Example: 1,3 or 1,2,4 or 5 for all): "
)

selected_tests = [c.strip() for c in choices.split(",")]


# =====================================================
# AI GENERATED TESTS
# =====================================================
if "4" in selected_tests or "5" in selected_tests:

    print("\nGenerating AI Database Tests...")

    ai_tests = generate_ai_tests(schema, llm)

    ai_tests = clean_sql(ai_tests)

    print("\nAI Generated SQL Tests:")
    print(ai_tests)

    ai_results = execute_ai_tests(cursor, ai_tests)

    results.extend(ai_results)


# =====================================================
# DATA QUALITY TESTS
# =====================================================
if "1" in selected_tests or "5" in selected_tests:

    print("\nRunning Data Quality Tests")

    for test_name, (check_query, fix_query) in data_quality_tests.items():

        print("\n--------------------------------")
        print("Test:", test_name)

        cursor.execute(check_query)
        rows = cursor.fetchall()

        if rows:

            print("Issue detected:", rows)

            try:
                explanation = llm.invoke(f"Explain this database issue: {rows}")
            except Exception:
                explanation = "AI explanation skipped"

            try:
                cursor.execute(fix_query)
                conn.commit()
                print("Self-healing fix applied")
            except Exception as e:
                print("Fix failed:", e)

            results.append((test_name, "FAILED", str(rows), explanation))

        else:

            results.append((test_name, "PASSED", "No issues found", ""))


# =====================================================
# ETL TESTS
# =====================================================
if "2" in selected_tests or "5" in selected_tests:

    print("\nRunning ETL Validation Checks")

    for check_name, query in etl_checks.items():

        print("\nETL Test:", check_name)

        cursor.execute(query)
        rows = cursor.fetchall()

        if rows:

            print("ETL issue detected:", rows)

            try:
                explanation = llm.invoke(f"Explain this ETL issue: {rows}")
            except Exception:
                explanation = "AI explanation skipped"

            results.append((check_name, "FAILED", str(rows), explanation))

        else:

            results.append((check_name, "PASSED", "Validation successful", ""))


# =====================================================
# AML TESTS
# =====================================================
if "3" in selected_tests or "5" in selected_tests:

    print("\nRunning AML Fraud Detection")

    for check_name, query in aml_checks.items():

        print("\nAML Check:", check_name)

        cursor.execute(query)
        rows = cursor.fetchall()

        if rows:

            print("Potential AML issue:", rows)

            try:
                explanation = llm.invoke(
                    f"Explain possible AML risk for these transactions: {rows}"
                )
            except Exception:
                explanation = "AI explanation skipped"

            results.append((check_name, "FAILED", str(rows), explanation))

        else:

            results.append((check_name, "PASSED", "No suspicious activity", ""))


# =====================================================
# CLOSE CONNECTION
# =====================================================
conn.close()

print("\n====================================")
print("AI Database Testing Completed")
print("====================================")


# =====================================================
# GENERATE REPORT
# =====================================================
generate_report(results)