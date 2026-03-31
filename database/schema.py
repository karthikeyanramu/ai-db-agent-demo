import sqlite3
from config.settings import DATABASE_PATH

# -------------------------------
# Database Connection
# -------------------------------
conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

# -------------------------------
# Table Definitions & Data
# -------------------------------
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
            (5, "Chen Wei", "chen.wei@email.com", "China", "Medium"),
            (6, "Carlos Diaz", "carlos.diaz@email.com", "Mexico", "Low"),
            (7, "Anna Schmidt", "anna.schmidt@email.com", "Germany", "Low"),
            (9, "Fatima Noor", "fatima.noor@email.com", "UAE", "Medium"),
            (10, "David Brown", "david.brown@email.com", "USA", "Low"),
            (11, "Raj Patel", "raj.patel2@email.com", "UAE", "High"),
            (12, "Mary Johnson", "mary.johnson2@email.com", "Russia", "High"),
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
            (104, 4, "Checking", 250000),
            (105, 5, "Savings", 15000),
            (112, 6, "Checking", -98),
            (107, 7, "Savings", 7000),
            (111, 8, "Checking", -45),
            (109, 9, "Savings", 20000),
            (110, 10, "Checking", 10000),
        ],
    },
    "transactions": {
        "drop": "DROP TABLE IF EXISTS transactions",
        "create": """
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY,
                account_id INTEGER,
                amount INTEGER,
                transaction_date TEXT
            )
        """,
        "indexes": [
            "CREATE INDEX IF NOT EXISTS idx_transactions_amount ON transactions(amount)",
            "CREATE INDEX IF NOT EXISTS idx_transactions_accounts ON transactions(account_id)",
        ],
        "data": [
            (1001, 101, 500, "2026-03-01"),
            (1002, 103, 2000, "2026-03-02"),
            (1003, 104, 50000, "2026-03-02"),
            (1004, 105, 1500, "2026-03-03"),
            (1005, 108, 70000, "2026-03-03"),
            (1006, 102, 800, "2026-03-04"),
            (1007, 109, 1200, "2026-03-04"),
            (1008, 110, 300, "2026-03-05"),
            (1009, 104, 45000, "2026-03-05"),
            (1010, 108, 60000, "2026-03-06"),
        ],
    },
    "raw_transactions": {
        "create": """
            CREATE TABLE IF NOT EXISTS raw_transactions(
                id INTEGER PRIMARY KEY,
                account_number INTEGER,
                amount TEXT,
                txn_date TEXT
            )
        """,
        "data": [
            (1, 101, "1000", "2026-03-01"),
            (2, 102, "2500", "2026-03-02"),
            (3, 103, "50000", "2026-03-02"),
            (4, 104, "0", "2026-03-03"),
            (5, 105, "900000", "2026-03-03"),
            (6, 106, "1200000", "2026-03-03"),
            (7, 107, "750", "2026-03-04"),
            (8, 108, "850", "2026-03-04"),
            (9, 109, "120", "2026-03-04"),
            (10, 110, "450", "2026-03-04"),
        ],
    },
    "aml_alerts": {
        "create": """
            CREATE TABLE IF NOT EXISTS aml_alerts (
                alert_id INTEGER PRIMARY KEY,
                transaction_id INTEGER,
                alert_type TEXT,
                status TEXT
            )
        """,
        "indexes": [
            "CREATE INDEX IF NOT EXISTS idx_alert_transaction ON aml_alerts(transaction_id)"
        ],
        "data": [
            (1, 1003, "Large Transaction", "Open"),
            (2, 1005, "Large Transaction", "Investigating"),
            (3, 1009, "Suspicious Pattern", "Open"),
            (4, 1010, "High Value Transfer", "Open"),
            (5, 1007, "Frequent Transfers", "Closed"),
            (6, 1004, "Medium Risk", "Closed"),
            (7, 1002, "Medium Risk", "Investigating"),
            (8, 1006, "Low Risk", "Closed"),
            (9, 1001, "Low Risk", "Closed"),
            (10, 1008, "Low Risk", "Closed"),
        ],
    },
}


conn.commit()

print("Database created successfully.")
conn.close()
