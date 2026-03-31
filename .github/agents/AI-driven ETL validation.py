import sqlite3
from langchain_community.llms import Ollama

print("AI ETL Validation Agent Started")

conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

llm = Ollama(model="llama3")

checks = {

"Source vs Target Record Count":

"""
SELECT
(SELECT COUNT(*) FROM raw_transactions),
(SELECT COUNT(*) FROM transactions)
""",

"Null Transaction Date":

"""
SELECT *
FROM transactions
WHERE transaction_date IS NULL
""",

"Zero Amount Transactions":

"""
SELECT *
FROM transactions
WHERE amount = 0
""",

"Duplicate Transactions":

"""
SELECT transaction_id, COUNT(*)
FROM transactions
GROUP BY transaction_id
HAVING COUNT(*) > 1
""",

"Large AML Transactions":

"""
SELECT *
FROM transactions
WHERE amount > 1000000
""",

"Invalid Account Reference":

"""
SELECT *
FROM transactions
WHERE account_id NOT IN
(SELECT account_id FROM accounts)
""",

"Future Transaction Dates":

"""
SELECT *
FROM transactions
WHERE transaction_date > DATE('now')
""",

"Transformation Accuracy":

"""
SELECT r.id, r.amount, t.amount
FROM raw_transactions r
JOIN transactions t
ON r.id = t.transaction_id
WHERE CAST(r.amount AS REAL) != t.amount
"""
}

for test_name, query in checks.items():

    print("\n--------------------------------")
    print("Running Test:", test_name)

    cursor.execute(query)
    rows = cursor.fetchall()

    if rows:

        print("Potential issue detected:")
        print(rows)

        try:

            explanation = llm.invoke(
            f"Explain the ETL validation issue: {rows}"
            )

            print("\nAI Analysis:")
            print(explanation)

        except:
            print("AI explanation skipped")

    else:

        print("No issue found")

conn.close()

print("\nETL Validation Completed")