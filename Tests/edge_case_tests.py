"""
Edge case and boundary condition tests for AI Database Agent
Tests unusual scenarios, data quality issues, and constraint violations
"""

import os
import sys
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.logger import setup_logger
from Agents.error_handler import safe_execute_query

logger = setup_logger(__name__)


def test_zero_balance_accounts(cursor):
    """Test detection of zero balance accounts"""
    try:
        query = "SELECT COUNT(*) as count FROM accounts WHERE balance = 0"
        result = safe_execute_query(cursor, query)
        
        if result is None:
            return {
                "name": "Zero Balance Detection",
                "passed": False,
                "result": "Query execution failed"
            }
        
        count = result[0][0]
        logger.info(f"Found {count} zero-balance accounts")
        
        return {
            "name": "Zero Balance Detection",
            "passed": True,
            "result": f"Found {count} zero-balance accounts"
        }
    except Exception as e:
        logger.error(f"Zero balance test failed: {e}")
        return {
            "name": "Zero Balance Detection",
            "passed": False,
            "result": str(e)
        }


def test_negative_balances(cursor):
    """Test detection of negative balances (overdrafts)"""
    try:
        query = "SELECT COUNT(*) as count FROM accounts WHERE balance < 0"
        result = safe_execute_query(cursor, query)
        
        if result is None:
            return {
                "name": "Negative Balance Detection",
                "passed": False,
                "result": "Query execution failed"
            }
        
        count = result[0][0]
        logger.info(f"Found {count} accounts with negative balance")
        
        return {
            "name": "Negative Balance Detection",
            "passed": True,
            "result": f"Found {count} overdraft accounts"
        }
    except Exception as e:
        logger.error(f"Negative balance test failed: {e}")
        return {
            "name": "Negative Balance Detection",
            "passed": False,
            "result": str(e)
        }


def test_orphaned_records(cursor):
    """Test detection of orphaned records (customers with no accounts)"""
    try:
        query = """
        SELECT COUNT(*) as count FROM customers c
        WHERE NOT EXISTS (SELECT 1 FROM accounts a WHERE a.customer_id = c.customer_id)
        """
        result = safe_execute_query(cursor, query)
        
        if result is None:
            return {
                "name": "Orphaned Records Detection",
                "passed": False,
                "result": "Query execution failed"
            }
        
        count = result[0][0]
        logger.info(f"Found {count} customers with no accounts")
        
        passed = count == 0  # Should have zero orphaned records
        return {
            "name": "Orphaned Records Detection",
            "passed": passed,
            "result": f"Found {count} orphaned customers (expected 0)"
        }
    except Exception as e:
        logger.error(f"Orphaned records test failed: {e}")
        return {
            "name": "Orphaned Records Detection",
            "passed": False,
            "result": str(e)
        }


def test_missing_customer_names(cursor):
    """Test detection of missing customer names"""
    try:
        query = """
        SELECT COUNT(*) as count FROM customers 
        WHERE name IS NULL OR TRIM(name) = ''
        """
        result = safe_execute_query(cursor, query)
        
        if result is None:
            return {
                "name": "Missing Customer Names",
                "passed": False,
                "result": "Query execution failed"
            }
        
        count = result[0][0]
        passed = count == 0  # Should have zero missing names
        
        logger.info(f"Found {count} customers with missing names")
        
        return {
            "name": "Missing Customer Names",
            "passed": passed,
            "result": f"Found {count} missing names (expected 0)"
        }
    except Exception as e:
        logger.error(f"Missing names test failed: {e}")
        return {
            "name": "Missing Customer Names",
            "passed": False,
            "result": str(e)
        }


def test_invalid_risk_ratings(cursor):
    """Test detection of invalid risk ratings"""
    try:
        # Valid risk ratings should be 'Low', 'Medium', 'High'
        query = """
        SELECT COUNT(*) as count FROM customers 
        WHERE risk_rating NOT IN ('Low', 'Medium', 'High')
        """
        result = safe_execute_query(cursor, query)
        
        if result is None:
            return {
                "name": "Invalid Risk Ratings",
                "passed": False,
                "result": "Query execution failed"
            }
        
        count = result[0][0]
        passed = count == 0  # Should have zero invalid ratings
        
        logger.info(f"Found {count} invalid risk ratings")
        
        return {
            "name": "Invalid Risk Ratings",
            "passed": passed,
            "result": f"Found {count} invalid ratings (expected 0)"
        }
    except Exception as e:
        logger.error(f"Invalid risk ratings test failed: {e}")
        return {
            "name": "Invalid Risk Ratings",
            "passed": False,
            "result": str(e)
        }


def test_zero_transaction_amounts(cursor):
    """Test detection of zero-value transactions"""
    try:
        query = """
        SELECT COUNT(*) as count FROM transactions 
        WHERE amount = 0
        """
        result = safe_execute_query(cursor, query)
        
        if result is None:
            return {
                "name": "Zero Transaction Amounts",
                "passed": False,
                "result": "Query execution failed"
            }
        
        count = result[0][0]
        logger.info(f"Found {count} zero-value transactions")
        
        return {
            "name": "Zero Transaction Amounts",
            "passed": True,
            "result": f"Found {count} zero-value transactions"
        }
    except Exception as e:
        logger.error(f"Zero transaction test failed: {e}")
        return {
            "name": "Zero Transaction Amounts",
            "passed": False,
            "result": str(e)
        }


def test_future_transactions(cursor):
    """Test detection of transactions with future dates"""
    try:
        query = """
        SELECT COUNT(*) as count FROM transactions 
        WHERE transaction_date > DATE('now')
        """
        result = safe_execute_query(cursor, query)
        
        if result is None:
            return {
                "name": "Future Transaction Detection",
                "passed": False,
                "result": "Query execution failed"
            }
        
        count = result[0][0]
        passed = count == 0  # Should have zero future transactions
        
        logger.info(f"Found {count} future-dated transactions")
        
        return {
            "name": "Future Transaction Detection",
            "passed": passed,
            "result": f"Found {count} future transactions (expected 0)"
        }
    except Exception as e:
        logger.error(f"Future transaction test failed: {e}")
        return {
            "name": "Future Transaction Detection",
            "passed": False,
            "result": str(e)
        }


def test_missing_transaction_dates(cursor):
    """Test detection of missing transaction dates"""
    try:
        query = """
        SELECT COUNT(*) as count FROM transactions 
        WHERE transaction_date IS NULL
        """
        result = safe_execute_query(cursor, query)
        
        if result is None:
            return {
                "name": "Missing Transaction Dates",
                "passed": False,
                "result": "Query execution failed"
            }
        
        count = result[0][0]
        passed = count == 0  # Should have zero missing dates
        
        logger.info(f"Found {count} transactions with missing dates")
        
        return {
            "name": "Missing Transaction Dates",
            "passed": passed,
            "result": f"Found {count} missing dates (expected 0)"
        }
    except Exception as e:
        logger.error(f"Missing dates test failed: {e}")
        return {
            "name": "Missing Transaction Dates",
            "passed": False,
            "result": str(e)
        }


def test_duplicate_transactions(cursor):
    """Test detection of duplicate transactions"""
    try:
        query = """
        SELECT COUNT(*) as count FROM (
            SELECT transaction_id, COUNT(*) as cnt 
            FROM transactions 
            GROUP BY transaction_id 
            HAVING cnt > 1
        )
        """
        result = safe_execute_query(cursor, query)
        
        if result is None:
            return {
                "name": "Duplicate Transactions Detection",
                "passed": False,
                "result": "Query execution failed"
            }
        
        count = result[0][0]
        passed = count == 0  # Should have zero duplicates
        
        logger.info(f"Found {count} duplicate transaction IDs")
        
        return {
            "name": "Duplicate Transactions Detection",
            "passed": passed,
            "result": f"Found {count} duplicate transaction IDs (expected 0)"
        }
    except Exception as e:
        logger.error(f"Duplicate transactions test failed: {e}")
        return {
            "name": "Duplicate Transactions Detection",
            "passed": False,
            "result": str(e)
        }


def test_account_transaction_consistency(cursor):
    """Test consistency between accounts and transactions"""
    try:
        query = """
        SELECT COUNT(*) as count FROM transactions t
        WHERE NOT EXISTS (SELECT 1 FROM accounts a WHERE a.account_id = t.account_id)
        """
        result = safe_execute_query(cursor, query)
        
        if result is None:
            return {
                "name": "Account-Transaction Consistency",
                "passed": False,
                "result": "Query execution failed"
            }
        
        count = result[0][0]
        passed = count == 0  # Should have zero orphaned transactions
        
        logger.info(f"Found {count} transactions referencing non-existent accounts")
        
        return {
            "name": "Account-Transaction Consistency",
            "passed": passed,
            "result": f"Found {count} orphaned transactions (expected 0)"
        }
    except Exception as e:
        logger.error(f"Account-transaction consistency test failed: {e}")
        return {
            "name": "Account-Transaction Consistency",
            "passed": False,
            "result": str(e)
        }


def run_all_edge_case_tests(cursor):
    """
    Run all edge case tests
    
    Args:
        cursor: SQLite cursor
    
    Returns:
        List of test results
    """
    logger.info("Starting Edge Case Tests...")
    
    tests = [
        test_zero_balance_accounts(cursor),
        test_negative_balances(cursor),
        test_orphaned_records(cursor),
        test_missing_customer_names(cursor),
        test_invalid_risk_ratings(cursor),
        test_zero_transaction_amounts(cursor),
        test_future_transactions(cursor),
        test_missing_transaction_dates(cursor),
        test_duplicate_transactions(cursor),
        test_account_transaction_consistency(cursor)
    ]
    
    logger.info(f"Edge Case Tests completed. Total: {len(tests)}")
    
    return tests


# If run directly, execute all tests
if __name__ == "__main__":
    import sqlite3
    from config import DATABASE_PATH
    
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        results = run_all_edge_case_tests(cursor)
        
        print("\n" + "="*60)
        print("EDGE CASE TEST RESULTS")
        print("="*60)
        
        for result in results:
            status = "✓ PASS" if result["passed"] else "✗ FAIL"
            print(f"{status} - {result['name']}: {result['result']}")
        
        print("="*60 + "\n")
        
        conn.close()
    except Exception as e:
        logger.error(f"Failed to run edge case tests: {e}")
