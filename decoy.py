from datetime import date
from sqlalchemy import Date
from database.db_handler import Transaction, get_all_transactions, save_transaction, get_transaction, update_transaction
transactions = get_all_transactions()

print(transactions[0])

transaction1 = Transaction(
    date=date(2024, 10, 14),
    type="Crédito",
    description="Pagamento de cliente: Caio",
    payment_method="Pix",
    bank="Inter",
    value=2004.90,
    categories=["Serviço", "Manutenção"],  # Lista de categorias como strings// podem ser uma lista das classes de Category tbm
    notes="Pagamento referente ao serviço de manutenção do equipamento X."
)
transaction1.id = 100

try:
    save_transaction(transaction1)
except Exception as e:
    print(e)

transaction2 = get_transaction(100)

transaction2.notes = "Pagamento referente ao serviço de manutenção do Acelerador de particulas."

print(transaction2)

update_transaction(transaction2)





