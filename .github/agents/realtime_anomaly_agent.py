import sqlite3
import time
from langchain_community.llms import Ollama

print("===================================")
print("Real-Time AI Anomaly Detection Agent")
print("===================================")

# Connect to database
conn = sqlite3.connect("aml_demo.db")
cursor = conn.cursor()

# Load Local AI Model
llm = Ollama(model="llama3")

last_checked_id = 0

try:

    while True:

        print("\nChecking for new transactions...")

        cursor.execute(
            """
            SELECT transaction_id, account_id, amount, transaction_date
            FROM transactions
            WHERE transaction_id > ?
            ORDER BY transaction_id
            """,
            (last_checked_id,)
        )

        new_transactions = cursor.fetchall()

        if new_transactions:

            for txn in new_transactions:

                txn_id, account_id, amount, date = txn

                print("\nNew Transaction Detected:")
                print(f"Transaction ID: {txn_id}, Account: {account_id}, Amount: {amount}, Date: {date}")

                # ---------------------------------
                # Rule 1: Large Transaction
                # ---------------------------------
                if amount > 1_000_000:

                    print("ANOMALY: Large Transaction Detected")

                    try:
                        analysis = llm.invoke(
                            f"A bank transaction of {amount} was detected for account {account_id}. "
                            "Explain possible AML risks such as money laundering or suspicious activity."
                        )

                        print("AI Risk Analysis:")
                        print(analysis)

                    except Exception as e:
                        print("AI analysis skipped:", e)

                # ---------------------------------
                # Rule 2: High Transaction Frequency
                # ---------------------------------
                cursor.execute(
                    """
                    SELECT COUNT(*)
                    FROM transactions
                    WHERE account_id = ?
                    """,
                    (account_id,)
                )

                txn_count = cursor.fetchone()[0]

                if txn_count > 5:
                    print("ANOMALY: High transaction frequency detected")

                # Update last checked id
                if txn_id > last_checked_id:
                    last_checked_id = txn_id

        else:

            print("No new transactions")

        # Wait before checking again
        time.sleep(5)

except KeyboardInterrupt:

    print("\nAgent stopped manually.")

finally:

    conn.close()
    print("Database connection closed.")