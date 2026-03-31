import sqlite3
from langchain_community.llms import Ollama

print("AI Self-Healing Database Agent Started")

# Connect to SQLite database
conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

# Local AI model (optional for generating explanation)
llm = Ollama(model="llama3")

# Test cases with detection query + fix query
tests = {

"Negative Balance":
(
"SELECT * FROM accounts WHERE balance < 0",
"UPDATE accounts SET balance = 0 WHERE balance < 0"
),

"Missing Transaction Date":
(
"SELECT * FROM transactions WHERE transaction_date IS NULL",
"UPDATE transactions SET transaction_date = DATE('now') WHERE transaction_date IS NULL"
),

"Zero Transaction Amount":
(
"SELECT * FROM transactions WHERE amount = 0",
"DELETE FROM transactions WHERE amount = 0"
),

"Duplicate Customers":
(
"""SELECT name, COUNT(*)
FROM customers
GROUP BY name
HAVING COUNT(*) > 1""",

"""DELETE FROM customers
WHERE rowid NOT IN (
SELECT MIN(rowid)
FROM customers
GROUP BY name
)"""
),

"Future Transaction Date":
(
"SELECT * FROM transactions WHERE transaction_date > DATE('now')",
"UPDATE transactions SET transaction_date = DATE('now') WHERE transaction_date > DATE('now')"
),

"Invalid Account Reference":
(
"""SELECT *
FROM transactions
WHERE from_account NOT IN
(SELECT account_id FROM accounts)""",

"""DELETE FROM transactions
WHERE from_account NOT IN
(SELECT account_id FROM accounts)"""
),

"Missing Customer Risk Rating":
(
"SELECT * FROM customers WHERE risk_rating IS NULL",
"UPDATE customers SET risk_rating='Medium' WHERE risk_rating IS NULL"
)

}

# Run tests
for test_name, (check_query, fix_query) in tests.items():

    print("\n----------------------------------")
    print("Running Test:", test_name)

    cursor.execute(check_query)
    rows = cursor.fetchall()

    if rows:

        print("Issue detected:", rows)

        # Ask AI to explain fix (for demo purpose)
        prompt = f"""
        Database issue detected:

        {rows}

        Explain what SQL fix should be applied.
        """

        try:
            explanation = llm.invoke(prompt)
            print("\nAI Explanation:")
            print(explanation)
        except:
            print("AI explanation skipped")

        # Apply fix
        try:
            cursor.execute(fix_query)
            conn.commit()
            print("Self-healing applied successfully")

        except Exception as e:
            print("Fix failed:", e)

    else:
        print("No issues found")

print("\nDatabase Health Check Completed")

conn.close()