# db_agent.py

import sqlite3
import sys
import os

# Add parent directory to path so we can import database module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.schema import tables
from config import DATABASE_PATH

# -------------------------------
# Connect to DB
# -------------------------------
conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

# -------------------------------
# Create tables, indexes, and insert data
# -------------------------------
for table_name, table_info in tables.items():
    if "drop" in table_info:
        cursor.execute(table_info["drop"])
    cursor.execute(table_info["create"])
    for index in table_info.get("indexes", []):
        cursor.execute(index)
    for row in table_info.get("data", []):
        placeholders = ','.join(['?']*len(row))
        cursor.execute(f"INSERT OR REPLACE INTO {table_name} VALUES ({placeholders})", row)

# -------------------------------
# Create Masked Customers View
# -------------------------------
cursor.execute("""
CREATE VIEW IF NOT EXISTS masked_customers AS
SELECT
    customer_id,
    SUBSTR(name,1,1) || '***' AS name,
    SUBSTR(email,1,2) || '***@***.com' AS email,
    risk_rating
FROM customers
""")

# -------------------------------
# Simulated ETL load
# -------------------------------
cursor.execute("""
INSERT OR IGNORE INTO transactions
SELECT
id,
account_number,
CAST(amount AS REAL),
txn_date
FROM raw_transactions
""")

conn.commit()
print("Database created successfully!")

# -------------------------------
# Optional: display table contents
# -------------------------------
def display_tables(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    for (table_name,) in cursor.fetchall():
        print(f"\nTable: {table_name}")
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in cursor.fetchall()]
        print("Columns:", columns)
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

display_tables(cursor)
conn.close()