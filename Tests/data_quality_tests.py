data_quality_tests = {

    "Negative Account Balance": (
        "SELECT * FROM accounts WHERE balance < 0",
        "UPDATE accounts SET balance = 0 WHERE balance < 0",
    ),

    "Missing Transaction Date": (
        "SELECT * FROM transactions WHERE transaction_date IS NULL",
        "UPDATE transactions SET transaction_date = DATE('now') WHERE transaction_date IS NULL",
    ),

    "Zero Transaction Amount": (
        "SELECT * FROM transactions WHERE amount = 0",
        "DELETE FROM transactions WHERE amount = 0",
    ),

    "Duplicate Transactions": (
        """SELECT transaction_id, COUNT(*) 
           FROM transactions 
           GROUP BY transaction_id 
           HAVING COUNT(*) > 1""",

        """DELETE FROM transactions 
           WHERE rowid NOT IN
           (SELECT MIN(rowid) FROM transactions GROUP BY transaction_id)""",
    ),

    "Future Transaction Dates": (
        "SELECT * FROM transactions WHERE transaction_date > DATE('now')",
        """UPDATE transactions 
           SET transaction_date = DATE('now')
           WHERE transaction_date > DATE('now')""",
    ),
}