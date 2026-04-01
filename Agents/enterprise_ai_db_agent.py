import os
import sys
import sqlite3

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_community.llms import Ollama
from config import DATABASE_PATH
from config.logger import setup_logger
from reporting.report_generator import generate_report

from Tests.data_quality_tests import data_quality_tests
from Tests.etl_tests import etl_checks
from Tests.aml_tests import aml_checks
from Tests.edge_case_tests import run_all_edge_case_tests

from Agents.error_handler import (
    validate_database_config,
    validate_sql_safe,
    validate_ai_response,
    safe_execute_query,
    DatabaseError,
    SQLSafetyError
)
from Agents.metrics import TestMetricsTracker

# Initialize logger
logger = setup_logger(__name__)

print("====================================")
print("Enterprise AI Database Testing Agent")
print("====================================")

logger.info("Starting Enterprise AI Database Testing Agent")


# -------------------------------
# CONNECT DATABASE
# -------------------------------
try:
    # Validate database configuration
    validate_database_config(DATABASE_PATH)
    logger.info(f"Database configuration validated: {DATABASE_PATH}")
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    logger.info("Database connected successfully")
    print("Database connected successfully")
except Exception as e:
    logger.error(f"Database connection failed: {e}")
    print("Database connection failed:", e)
    sys.exit()


# Load AI model
try:
    llm = Ollama(model="llama3")
    logger.info("AI Model (Llama3) loaded successfully")
except Exception as e:
    logger.error(f"Failed to load AI model: {e}")
    print("Warning: Could not load AI model. Some features may be disabled.")
    llm = None

results = []
metrics_tracker = TestMetricsTracker()


# =====================================================
# CLEAN AI SQL OUTPUT
# =====================================================
def clean_sql(ai_response):
    cleaned = ai_response.replace("```sql", "")
    cleaned = cleaned.replace("```", "")
    cleaned = cleaned.strip()
    logger.debug(f"Cleaned SQL: {cleaned[:100]}...")
    return cleaned


# =====================================================
# VALIDATE SAFE SQL
# =====================================================
def is_safe_query(query):
    try:
        validate_sql_safe(query)
        return True
    except SQLSafetyError:
        return False


# =====================================================
# SCHEMA DISCOVERY
# =====================================================
def discover_schema(cursor):
    schema_info = {}
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            schema_info[table_name] = [col[1] for col in columns]
        
        logger.info(f"Schema discovery completed. Found {len(tables)} tables")
    except Exception as e:
        logger.error(f"Schema discovery failed: {e}")
    
    return schema_info


# =====================================================
# AI TEST GENERATOR
# =====================================================
def generate_ai_tests(schema, llm):
    if llm is None:
        logger.warning("AI model not available. Skipping AI test generation")
        return ""
    
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
    
    try:
        response = llm.invoke(prompt)
        logger.info("AI test generation completed")
        return response
    except Exception as e:
        logger.error(f"AI test generation failed: {e}")
        return ""


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
            logger.warning(f"Blocked unsafe query: {query}")
            continue
        
        logger.debug(f"Running AI Test: {query[:100]}...")
        
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            
            if rows:
                logger.warning(f"AI Issue detected: {rows}")
                ai_results.append(
                    ("AI Generated Test", "FAILED", str(rows), "AI detected issue")
                )
            else:
                ai_results.append(
                    ("AI Generated Test", "PASSED", "No issue found", "")
                )
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
    
    return ai_results


# =====================================================
# DISCOVER DATABASE
# =====================================================
logger.info("Discovering Database Schema...")
print("\nDiscovering Database Schema...")

schema = discover_schema(cursor)

for table, columns in schema.items():
    logger.info(f"Table Found: {table} -> {columns}")
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
print("4 - Edge Case Tests (NEW)")
print("5 - AI Generated Tests")
print("6 - Run All Tests")

choices = input(
    "\nEnter test numbers separated by comma (Example: 1,3 or 1,2,4 or 6 for all): "
)

selected_tests = [c.strip() for c in choices.split(",")]

# Start timing all tests
metrics_tracker.overall_metrics.start()

logger.info(f"Selected test groups: {selected_tests}")


# =====================================================
# AI GENERATED TESTS
# =====================================================
if "5" in selected_tests or "6" in selected_tests:
    print("\nGenerating AI Database Tests...")
    logger.info("Starting AI Generated Tests")
    
    metrics_tracker.overall_metrics.record_test("AI Generated Tests", None)
    
    if llm is not None:
        ai_tests = generate_ai_tests(schema, llm)
        ai_tests = clean_sql(ai_tests)
        
        print("\nAI Generated SQL Tests:")
        print(ai_tests)
        logger.info(f"AI Generated SQL: {ai_tests[:200]}...")
        
        ai_results = execute_ai_tests(cursor, ai_tests)
        results.extend(ai_results)
        
        # Record AI test results
        for result in ai_results:
            passed = result[1] == "PASSED"
            metrics_tracker.overall_metrics.record_test(result[0], passed, result[2])
    else:
        logger.warning("AI model not available. Skipping AI Generated Tests")
        print("AI model not available. Skipping AI Generated Tests")


# =====================================================
# DATA QUALITY TESTS
# =====================================================
if "1" in selected_tests or "6" in selected_tests:
    print("\nRunning Data Quality Tests")
    logger.info("Starting Data Quality Tests")
    metrics_tracker.data_quality_metrics.start()
    
    for test_name, (check_query, fix_query) in data_quality_tests.items():
        print("\n--------------------------------")
        print("Test:", test_name)
        logger.info(f"Running Data Quality Test: {test_name}")
        
        try:
            cursor.execute(check_query)
            rows = cursor.fetchall()
            
            if rows:
                print("Issue detected:", rows)
                logger.warning(f"{test_name}: Issue detected: {rows}")
                
                explanation = "No explanation available"
                if llm is not None:
                    try:
                        explanation = llm.invoke(f"Explain this database issue: {rows}")
                    except Exception as e:
                        logger.debug(f"AI explanation failed: {e}")
                
                try:
                    cursor.execute(fix_query)
                    conn.commit()
                    print("Self-healing fix applied")
                    logger.info(f"{test_name}: Self-healing fix applied")
                except Exception as e:
                    logger.error(f"{test_name}: Fix failed: {e}")
                    print("Fix failed:", e)
                
                results.append((test_name, "FAILED", str(rows), explanation))
                metrics_tracker.data_quality_metrics.record_test(test_name, False, str(rows))
            else:
                results.append((test_name, "PASSED", "No issues found", ""))
                metrics_tracker.data_quality_metrics.record_test(test_name, True, "No issues")
        
        except Exception as e:
            logger.error(f"{test_name}: Execution error: {e}")
            metrics_tracker.data_quality_metrics.record_test(test_name, False, str(e))
    
    metrics_tracker.data_quality_metrics.end()


# =====================================================
# ETL TESTS
# =====================================================
if "2" in selected_tests or "6" in selected_tests:
    print("\nRunning ETL Validation Checks")
    logger.info("Starting ETL Tests")
    metrics_tracker.etl_metrics.start()
    
    for check_name, query in etl_checks.items():
        print("\nETL Test:", check_name)
        logger.info(f"Running ETL Test: {check_name}")
        
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            
            if rows:
                print("ETL issue detected:", rows)
                logger.warning(f"{check_name}: ETL issue detected: {rows}")
                
                explanation = "No explanation available"
                if llm is not None:
                    try:
                        explanation = llm.invoke(f"Explain this ETL issue: {rows}")
                    except Exception as e:
                        logger.debug(f"AI explanation failed: {e}")
                
                results.append((check_name, "FAILED", str(rows), explanation))
                metrics_tracker.etl_metrics.record_test(check_name, False, str(rows))
            else:
                results.append((check_name, "PASSED", "Validation successful", ""))
                metrics_tracker.etl_metrics.record_test(check_name, True, "Valid")
        
        except Exception as e:
            logger.error(f"{check_name}: Execution error: {e}")
            metrics_tracker.etl_metrics.record_test(check_name, False, str(e))
    
    metrics_tracker.etl_metrics.end()


# =====================================================
# AML TESTS
# =====================================================
if "3" in selected_tests or "6" in selected_tests:
    print("\nRunning AML Fraud Detection")
    logger.info("Starting AML Tests")
    metrics_tracker.aml_metrics.start()
    
    for check_name, query in aml_checks.items():
        print("\nAML Check:", check_name)
        logger.info(f"Running AML Test: {check_name}")
        
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            
            if rows:
                print("Potential AML issue:", rows)
                logger.warning(f"{check_name}: AML alert: {rows}")
                
                explanation = "No explanation available"
                if llm is not None:
                    try:
                        explanation = llm.invoke(
                            f"Explain possible AML risk for these transactions: {rows}"
                        )
                    except Exception as e:
                        logger.debug(f"AI explanation failed: {e}")
                
                results.append((check_name, "FAILED", str(rows), explanation))
                metrics_tracker.aml_metrics.record_test(check_name, False, str(rows))
            else:
                results.append((check_name, "PASSED", "No suspicious activity", ""))
                metrics_tracker.aml_metrics.record_test(check_name, True, "Safe")
        
        except Exception as e:
            logger.error(f"{check_name}: Execution error: {e}")
            metrics_tracker.aml_metrics.record_test(check_name, False, str(e))
    
    metrics_tracker.aml_metrics.end()


# =====================================================
# EDGE CASE TESTS
# =====================================================
if "4" in selected_tests or "6" in selected_tests:
    print("\nRunning Edge Case Tests")
    logger.info("Starting Edge Case Tests")
    metrics_tracker.edge_case_metrics.start()
    
    edge_case_results = run_all_edge_case_tests(cursor)
    
    for result in edge_case_results:
        print(f"Edge Case - {result['name']}: {result['result']}")
        results.append((
            f"Edge Case - {result['name']}", 
            "PASSED" if result['passed'] else "FAILED",
            result['result'],
            ""
        ))
        metrics_tracker.edge_case_metrics.record_test(
            result['name'], 
            result['passed'], 
            result['result']
        )
    
    metrics_tracker.edge_case_metrics.end()


# End overall timing
metrics_tracker.overall_metrics.end()


# =====================================================
# CLOSE CONNECTION
# =====================================================
try:
    conn.close()
    logger.info("Database connection closed successfully")
except Exception as e:
    logger.error(f"Error closing database connection: {e}")

print("\n====================================")
print("AI Database Testing Completed")
print("====================================")

# Print metrics summaries
print("\n\n*** PERFORMANCE METRICS ***")
metrics_tracker.data_quality_metrics.print_summary()
metrics_tracker.etl_metrics.print_summary()
metrics_tracker.aml_metrics.print_summary()
metrics_tracker.edge_case_metrics.print_summary()
metrics_tracker.overall_metrics.print_summary()

logger.info("All testing completed successfully")

# =====================================================
# GENERATE REPORT
# =====================================================
execution_time = metrics_tracker.overall_metrics.results.get("execution_time", None)
report_path = generate_report(results, execution_time)