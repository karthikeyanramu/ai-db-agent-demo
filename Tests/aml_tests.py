aml_checks = {

    "Large Suspicious Transactions": """
        SELECT *
        FROM transactions
        WHERE amount > 1000000
    """,

    "Frequent Transactions": """
        SELECT account_id, COUNT(*)
        FROM transactions
        GROUP BY account_id
        HAVING COUNT(*) > 5
    """,

    "High Risk Customer Transactions": """
        SELECT c.name, t.amount
        FROM customers c
        JOIN accounts a
        ON c.customer_id = a.customer_id
        JOIN transactions t
        ON a.account_id = t.account_id
        WHERE c.risk_rating = 'High'
        AND t.amount > 50000
    """,
}