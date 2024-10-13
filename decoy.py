from database.db_handler import get_all_transactions
transactions = get_all_transactions()

print(transactions[0])