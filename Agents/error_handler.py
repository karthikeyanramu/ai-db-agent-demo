"""
Error handling and validation for AI Database Agent
Provides custom exceptions and validation functions
"""

import os
import sys
from config.logger import setup_logger

logger = setup_logger(__name__)


# =====================================================
# CUSTOM EXCEPTIONS
# =====================================================

class DatabaseError(Exception):
    """Raised when database operation fails"""
    pass


class AIValidationError(Exception):
    """Raised when AI response validation fails"""
    pass


class SQLSafetyError(Exception):
    """Raised when SQL contains dangerous commands"""
    pass


class ConfigurationError(Exception):
    """Raised when configuration is invalid"""
    pass


# =====================================================
# VALIDATION FUNCTIONS
# =====================================================

def validate_sql_safe(query):
    """
    Validate SQL query before execution
    Prevents dangerous operations like DROP, DELETE, etc.
    
    Args:
        query: SQL query string
    
    Returns:
        True if query is safe
    
    Raises:
        SQLSafetyError: If query contains dangerous keywords
    """
    
    # Dangerous SQL keywords that should not be executed
    dangerous_keywords = [
        "DROP",
        "DELETE",
        "UPDATE",
        "INSERT",
        "ALTER",
        "TRUNCATE",
        "GRANT",
        "REVOKE",
        "CREATE",
        "REPLACE"
    ]
    
    query_upper = query.upper().strip()
    
    for keyword in dangerous_keywords:
        if keyword in query_upper:
            logger.warning(f"Dangerous SQL keyword detected: {keyword}")
            raise SQLSafetyError(
                f"Query contains dangerous keyword: {keyword}. "
                f"Only SELECT queries are allowed."
            )
    
    return True


def validate_ai_response(response):
    """
    Validate AI-generated response
    Ensures response contains SQL and doesn't have dangerous keywords
    
    Args:
        response: AI model response string
    
    Returns:
        Tuple (is_valid: bool, message: str)
    """
    
    if not response or len(response.strip()) == 0:
        return False, "Empty response from AI model"
    
    # Check if response contains SQL keywords
    sql_keywords = ["SELECT", "WHERE", "FROM", "JOIN", "GROUP", "ORDER", "LIMIT"]
    has_sql = any(keyword in response.upper() for keyword in sql_keywords)
    
    if not has_sql:
        return False, "Response doesn't contain valid SQL keywords"
    
    # Check for dangerous keywords
    try:
        validate_sql_safe(response)
    except SQLSafetyError as e:
        return False, str(e)
    
    # Check for syntax validity
    if response.count("(") != response.count(")"):
        return False, "Unmatched parentheses in SQL"
    
    if response.count("'") % 2 != 0:
        return False, "Unmatched quotes in SQL"
    
    return True, "Valid SQL response"


def validate_database_config(db_path):
    """
    Validate database configuration
    
    Args:
        db_path: Path to database file
    
    Returns:
        True if configuration is valid
    
    Raises:
        ConfigurationError: If configuration is invalid
    """
    
    db_dir = os.path.dirname(db_path)
    
    if not os.path.exists(db_dir):
        try:
            os.makedirs(db_dir, exist_ok=True)
            logger.info(f"Created database directory: {db_dir}")
        except Exception as e:
            raise ConfigurationError(f"Cannot create database directory: {e}")
    
    return True


def safe_execute_query(cursor, query):
    """
    Execute SQL query with error handling
    
    Args:
        cursor: SQLite cursor
        query: SQL query string
    
    Returns:
        Query results or None if error
    """
    
    try:
        validate_sql_safe(query)
        logger.debug(f"Executing query: {query[:100]}...")
        cursor.execute(query)
        results = cursor.fetchall()
        logger.debug(f"Query returned {len(results)} rows")
        return results
    
    except SQLSafetyError as e:
        logger.error(f"SQL Safety Error: {e}")
        return None
    
    except Exception as e:
        logger.error(f"Database Error: {type(e).__name__}: {e}")
        return None


def safe_execute_update(cursor, conn, query):
    """
    Execute UPDATE/INSERT query with error handling
    
    Args:
        cursor: SQLite cursor
        conn: SQLite connection
        query: SQL query string
    
    Returns:
        Number of rows affected or -1 if error
    """
    
    try:
        logger.info(f"Executing update: {query[:100]}...")
        cursor.execute(query)
        conn.commit()
        rows_affected = cursor.rowcount
        logger.info(f"Update completed. Rows affected: {rows_affected}")
        return rows_affected
    
    except Exception as e:
        conn.rollback()
        logger.error(f"Update Error: {type(e).__name__}: {e}")
        return -1


# =====================================================
# ERROR REPORTING
# =====================================================

def format_error(exception, context=""):
    """
    Format error message for logging
    
    Args:
        exception: Exception object
        context: Additional context string
    
    Returns:
        Formatted error message
    """
    
    error_msg = f"{type(exception).__name__}: {str(exception)}"
    if context:
        error_msg = f"{context} - {error_msg}"
    
    return error_msg
