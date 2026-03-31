etl_checks = {

    "Source vs Target Record Count": """
        SELECT
        (SELECT COUNT(*) FROM raw_transactions),
        (SELECT COUNT(*) FROM transactions)
    """,

    "Transformation Accuracy": """
        SELECT r.id, r.amount, t.amount
        FROM raw_transactions r
        JOIN transactions t
        ON r.id = t.transaction_id
        WHERE CAST(r.amount AS REAL) != t.amount
    """,

    "Null Transaction Dates": """
        SELECT * 
        FROM transactions 
        WHERE transaction_date IS NULL
    """,
}