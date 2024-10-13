import os
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

    def __str__(self):
        categories_str = ', '.join([category.name for category in self.categories])  # Converte categorias em string
        return (f"Transaction(id={self.id}, date={self.date}, type={self.type}, "
                f"description={self.description}, payment_method={self.payment_method}, "
                f"bank={self.bank}, value={self.value}, categories=[{categories_str}], "
                f"notes={self.notes})")

# Criação do banco de dados e das tabelas
Base.metadata.create_all(engine)

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
