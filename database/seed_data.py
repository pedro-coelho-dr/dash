from db_handler import add_transaction, clear_transactions, add_category, get_all_categories
from datetime import date, timedelta
import random
from db_handler import PaymentMethodEnum, TransactionTypeEnum, BankEnum

# Função para popular o banco de dados com 30 entradas de exemplo
def seed_data():
    # Limpar o banco de dados antes de popular
    clear_transactions()

    # Definir algumas categorias iniciais
    predefined_categories = ['Venda de Produto', 'Serviço', 'Materiais', 'Salário', 'Manutenção']

    # Adicionar as categorias no banco de dados
    for category in predefined_categories:
        add_category(category)

    # Buscar todas as categorias disponíveis no banco de dados
    available_categories = get_all_categories()

    # Definir algumas descrições para as transações
    descriptions = ['Venda A', 'Conserto', 'Compra Material', 'Salário Mensal', 'ReAparo Máquina']

    # Gerar 30 transações de exemplo
    start_date = date(2024, 9, 1)  # Data de início das transações

    for i in range(30):
        # Gerar dados aleatórios para a transação
        trans_date = start_date + timedelta(days=i)  # Incrementa cada transação em 1 dia
        
        # Escolher entre CREDITO e DEBITO (com os valores exatos do Enum)
        type_ = random.choice([TransactionTypeEnum.CREDITO, TransactionTypeEnum.DEBITO])  
        
        # Valor entre 100 e 2000
        value = round(random.uniform(100, 2000), 2)  

        # Descrição aleatória
        description = random.choice(descriptions)
        
        # Selecionar um método de pagamento do enum PaymentMethodEnum
        payment_method = random.choice(list(PaymentMethodEnum))  # Usar os valores exatos do Enum
        
        # Selecionar um banco do enum BankEnum
        bank = random.choice(list(BankEnum))  # Usar os valores exatos do Enum
        
        # Escolher 1 a 3 categorias aleatórias
        categories = random.sample(available_categories, random.randint(1, 3))
        
        # Aleatoriamente adicionar notas
        notes = 'Notas de teste' if random.random() > 0.5 else ''  

        # Adicionar a transação ao banco de dados
        add_transaction(
            date=trans_date,
            type_=type_,
            description=description,
            payment_method=payment_method,
            bank=bank,
            value=value,
            categories=categories,  # Associar categorias
            notes=notes
        )
        print(f"Adicionada transação {i + 1}: {description}, {value}, {type_.value}, Categorias: {categories}")

# Chamar a função para popular os dados
if __name__ == '__main__':
    seed_data()
    print("Banco de dados populado com 30 entradas de exemplo.")
