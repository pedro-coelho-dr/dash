import os
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Text, Enum, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import enum

# diretório base e caminho do banco de dados
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'database.db')

# SQLAlchemy
engine = create_engine(f'sqlite:///{DATABASE_PATH}')
Session = sessionmaker(bind=engine)
session = Session()

# Base modelos do SQLAlchemy/ classe mae para fazer registros de outras classes modelos no banco
Base = declarative_base()

# Bancos
class BankEnum(enum.Enum):
    CRED_CREA = "Cred Crea"
    INTER = "Inter"
    CAIXA = "Caixa"

# Tipo de Transação
class TransactionTypeEnum(enum.Enum):
    CREDITO = "Crédito"
    DEBITO = "Débito"

# Método de Pagamento
class PaymentMethodEnum(enum.Enum): 
    PIX = "Pix"
    DEBITO = "Débito"
    CREDITO = "Crédito"
    DINHEIRO = "Dinheiro"
    BOLETO = "Boleto"
    TRANSFERENCIA = "Transferência"

# Tabela de associação para relacionamento N:N
transaction_category_association = Table(
    'transaction_category', Base.metadata,
    Column('transaction_id', Integer, ForeignKey('transactions.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)

# Modelo Category para armazenar categorias dinamicamente
class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

# Modelo Transaction
class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)  # Id
    date = Column(Date)  # Data da transação
    type = Column(String)  # Crédito ou Débito
    description = Column(String)  # Nome da origem/destino da transação
    payment_method = Column(String)  # Forma de pagamento
    bank = Column(String)  # Banco
    value = Column(Float)  # Valor da transação
    categories = relationship("Category", secondary=transaction_category_association)  # Lista de Category/ Relacionamento N:N
    notes = Column(Text)  # Observações

    def __init__(self, date:Date, type:String, description:String, payment_method:String, bank:String, value:Float, categories:list[Category], notes:Text):
        # Chama o construtor da classe Base (declarative_base) para garantir a compatibilidade com o SQLAlchemy
        super(Transaction, self).__init__()


        # caso categorias seja uma lista de strings
        if isinstance(categories, list) and all(isinstance(cat, str) for cat in categories):
            # Verificar e criar categorias, se necessário
            category_objects = []
            for category_name in categories:
                category = session.query(Category).filter_by(name=category_name).first()

                if not category:
                    category = Category(name=category_name)
                    session.add(category)

                category_objects.append(category)
            
            categories = category_objects
        

        # Defina os atributos
        self.date = date
        self.type = type
        self.description = description
        self.payment_method = payment_method
        self.bank = bank
        self.value = value
        self.categories = categories
        self.notes = notes

    def __str__(self):
        categories_str = ', '.join([category.name for category in self.categories])  # Converte categorias em string
        return (f"Transaction(id={self.id}, date={self.date}, type={self.type}, "
                f"description={self.description}, payment_method={self.payment_method}, "
                f"bank={self.bank}, value={self.value}, categories=[{categories_str}], "
                f"notes={self.notes})")



# Criação do banco de dados e das tabelas
Base.metadata.create_all(engine)

#====CRUD====

# Função para salvar transações
def save_transaction(transaction):
    try:
        session.add(transaction)
        session.commit()
    except Exception as e:
        session.rollback()  # Desfaz qualquer mudança em caso de erro
        raise ValueError(f"Error saving transaction: {e}")

# Função para obter uma transação pelo ID
def get_transaction(id):
    try:
        transaction = session.query(Transaction).filter_by(id=id).first()
        if transaction is None:
            raise ValueError(f"Transaction with id {id} not found.")
        
        return transaction
    
    except Exception as e:
        raise ValueError(f"Error retrieving transaction: {e}")

# Função para editar transações
def update_transaction(transaction):
    try:
        persisted_transaction = get_transaction(transaction.id)
        
        # Modifica os atributos da transação
        persisted_transaction.date = transaction.date
        persisted_transaction.type = transaction.type
        persisted_transaction.description = transaction.description
        persisted_transaction.payment_method = transaction.payment_method
        persisted_transaction.bank = transaction.bank
        persisted_transaction.value = transaction.value
        persisted_transaction.categories = transaction.categories
        persisted_transaction.notes = transaction.notes
        
        # As alterações feitas em 'persisted_transaction' são automaticamente detectadas
        session.commit()  # As mudanças são persistidas no banco de dados

    except Exception as e:
        session.rollback()  # Desfaz qualquer mudança em caso de erro
        raise ValueError(f"Error editing transaction: {e}") # Re-raise se a transação não for encontrada


# Função para adicionar transações
def add_transaction(date, type_, description, payment_method, bank, value, categories, notes): # as categorias são uma lista de nomes
    # Verificar e criar categorias, se necessário
    category_objects = []
    for category_name in categories:
        category = session.query(Category).filter_by(name=category_name).first()
        if not category:
            category = Category(name=category_name)
            session.add(category)
        category_objects.append(category)

    new_transaction = Transaction(
        date=date,
        type=type_, 
        description=description,
        payment_method=payment_method,
        bank=bank,
        value=value,
        categories=category_objects,  # Associar categorias
        notes=notes
    )
    session.add(new_transaction)
    session.commit()

# Função para adicionar uma nova categoria
def add_category(name):
    if not session.query(Category).filter_by(name=name).first():
        new_category = Category(name=name)
        session.add(new_category)
        session.commit()

# Função para buscar todas as categorias
def get_all_categories():
    return [category.name for category in session.query(Category).all()]

# Função para buscar todas as transações
def get_all_transactions():
    return session.query(Transaction).all()

# Função para limpar todas as transações do banco de dados
def clear_transactions():
    session.query(Transaction).delete()
    session.commit()
    print("Database cleared.")


def get_Transactions_Dataframe():
    # Buscar transações do banco de dados
    transactions = get_all_transactions()

    # Converter registros de transações para um DataFrame do Pandas
    if transactions:
        transaction_data = {
            "ID": [],
            "Data": [],
            "Tipo": [],
            "Descrição": [],
            "Método de Pagamento": [],
            "Banco": [],
            "Valor": [],
            "Categorias": [],
            "Notas": []
        }
        
        # Armazenar todas as transações no dicionário por coluna
        for t in transactions:
            transaction_data["ID"].append(t.id)
            transaction_data["Data"].append(t.date)
            transaction_data["Tipo"].append("Receita" if t.type == TransactionTypeEnum.CREDITO.name else "Despesa")
            transaction_data["Descrição"].append(t.description)
            transaction_data["Método de Pagamento"].append(t.payment_method)
            transaction_data["Banco"].append(t.bank)
            transaction_data["Valor"].append(t.value)
            transaction_data["Categorias"].append(", ".join([cat.name for cat in t.categories]))
            transaction_data["Notas"].append(t.notes)

    # Criar DataFrame com dicionário
    df_transactions = pd.DataFrame(transaction_data)
    # Normalizar dados
    df_transactions['Data'] = pd.to_datetime(df_transactions['Data'])  # Certificar que 'Data' está no formato datetime
    
    return df_transactions

# Função para deletar uma transação pelo ID
def delete_transaction(id):
    try:
        # Procurar a transação pelo ID
        transaction = session.query(Transaction).filter_by(id=id).first()
        if not transaction:
            raise ValueError(f"Transaction with id {id} not found.")
        
        # Deletar a transação
        session.delete(transaction)
        session.commit()
        print(f"Transaction with id {id} deleted.")
        
    except Exception as e:
        session.rollback()  # Desfaz qualquer mudança em caso de erro
        raise ValueError(f"Error deleting transaction: {e}")
