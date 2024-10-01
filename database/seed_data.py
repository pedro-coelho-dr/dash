from db_handler import add_transaction, clear_transactions
from datetime import date, timedelta
import random


# Function to populate the database with 30 sample data entries
def seed_data():
    # Clear the database before seeding
    clear_transactions()

    # Define some sample categories, descriptions, and payment methods
    categories = ['Venda de Produto', 'Serviço', 'Materiais', 'Salário', 'Manutenção']
    descriptions = ['Venda A', 'Conserto', 'Compra Material', 'Salário Mensal', 'ReAparo Máquina']
    payment_methods = ['Dinheiro', 'Crédito', 'Boleto', 'Transferência Bancária']

    # Generate 30 sample transactions
    start_date = date(2024, 9, 1)  # Starting date for transactions

    for i in range(30):
        # Generate random transaction data
        trans_date = start_date + timedelta(days=i)  # Increment each transaction by 1 day
        type_ = random.choice(['Receita', 'Despesa'])  # Randomly choose Receita or Despesa
        value = round(random.uniform(100, 2000), 2)  # Random value between 100 and 2000
        category = random.choice(categories)
        description = random.choice(descriptions)
        payment_method = random.choice(payment_methods)
        document_number = str(random.randint(10000, 99999))  # Random 5-digit document number
        responsible = random.choice(['João', 'Maria', 'Carlos', 'Ana'])
        notes = 'Notas de teste' if random.random() > 0.5 else ''  # Randomly add notes

        # Add the transaction to the database
        add_transaction(
            date=trans_date,
            type_=type_,
            value=value,
            category=category,
            description=description,
            payment_method=payment_method,
            document_number=document_number,
            responsible=responsible,
            notes=notes
        )
        print(f"Added transaction {i + 1}: {description}, {value}, {type_}")

# Call the function to seed the data
if __name__ == '__main__':
    seed_data()
    print("Database populated with 30 sample entries.")