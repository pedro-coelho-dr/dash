import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Definindo o diretório base e o caminho para o banco de dados
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'database.db')

# SQLAlchemy
engine = create_engine(f'sqlite:///{DATABASE_PATH}')
Session = sessionmaker(bind=engine)
session = Session()

# Base para os modelos do SQLAlchemy
Base = declarative_base()

# Modelo
class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)  # Identificador da transação
    date = Column(Date)  # Data da transação
    type = Column(String)  # Tipo: Receita ou Despesa
    description = Column(String)  # Descrição (ex.: origem ou fornecedor)
    payment_method = Column(String)  # Forma de pagamento (ex.: Transferência, Crédito)
    bank = Column(String)  # Banco (ex.: Banco do Brasil, Caixa)
    value = Column(Float)  # Valor da transação
    category = Column(String)  # Categoria (ex.: Materiais, Serviços)
    notes = Column(Text)  # Observações (opcional)

# Criação do banco de dados e das tabelas
Base.metadata.create_all(engine)

# Função para adicionar transações
def add_transaction(date, type_, description, payment_method, bank, value, category, notes):
    new_transaction = Transaction(
        date=date,
        type=type_,
        description=description,
        payment_method=payment_method,
        bank=bank,
        value=value,
        category=category,
        notes=notes
    )
    session.add(new_transaction)
    session.commit()

# Função para buscar todas as transações
def get_all_transactions():
    return session.query(Transaction).all()

# Função para limpar todas as transações do banco de dados
def clear_transactions():
    session.query(Transaction).delete()
    session.commit()
    print("Database cleared.")