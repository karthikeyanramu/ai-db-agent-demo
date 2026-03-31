from langchain_community.utilities import SQLDatabase

# connect database
db = SQLDatabase.from_uri("sqlite:///bank.db")

tests = {

"Negative Balance Test":
"SELECT * FROM accounts WHERE balance < 0",

"High Value Transaction Test":
"SELECT * FROM transactions WHERE amount > 100000",

"Transactions referencing non-existing accounts":
"SELECT * FROM transactions WHERE from_account NOT IN (SELECT account_id FROM accounts);",

"Duplicate customer records":
"SELECT name, COUNT(*) FROM customers GROUP BY name HAVING COUNT(*) > 1;",

"Missing Transaction Date":
"SELECT * FROM transactions WHERE transaction_date IS NULL",

"Zero Transaction Amount":
"SELECT * FROM transactions WHERE amount = 0",

"Frequent Transactions":
"""SELECT from_account, COUNT(*) FROM transactions
GROUP BY from_account HAVING COUNT(*) > 5""",

"Customers Without Accounts":
"""SELECT * FROM customers WHERE customer_id NOT IN
(SELECT customer_id FROM accounts)""",

"Accounts Without Transactions":
"""SELECT * FROM accounts WHERE account_id NOT IN
(SELECT from_account FROM transactions)"""

}

print("Autonomous Database Testing Agent Started")

for test, query in tests.items():

    print("\nRunning:", test)

    result = db.run(query)

    if result == "" or result == "[]":
        print("Status: PASSED")
    else:
        print("Status: FAILED")
        print("Issue Found:", result)