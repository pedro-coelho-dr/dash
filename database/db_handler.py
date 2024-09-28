import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'database.db')

# SQLAlchemy
engine = create_engine(f'sqlite:///{DATABASE_PATH}')
Session = sessionmaker(bind=engine)
session = Session()

# Base para os models do SQLAlchemy
Base = declarative_base()

# Model para transações financeiras (despesas e receitas)
class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    date = Column(Date)                      # Data da transação (recebimento ou despesa)
    type = Column(String)                    # Tipo: Receita ou Despesa
    value = Column(Float)                    # Valor da transação
    category = Column(String)                # Categoria (ex.: Materiais, Serviços)
    description = Column(String)             # Descrição (Origem para receita, Fornecedor para despesa)
    payment_method = Column(String)          # Forma de pagamento (ex.: Transferência, Crédito)
    document_number = Column(String)         # Número do documento
    responsible = Column(String)             # Responsável
    notes = Column(Text)                     # Observações (opcional)

# Criação do banco de dados e das tabelas
Base.metadata.create_all(engine)

# Função para adicionar transações
def add_transaction(date, type_, value, category, description, payment_method, document_number, responsible, notes):
    new_transaction = Transaction(
        date=date,
        type=type_,
        value=value,
        category=category,
        description=description,
        payment_method=payment_method,
        document_number=document_number,
        responsible=responsible,
        notes=notes
    )
    session.add(new_transaction)
    session.commit()

# Função para buscar todas as transações
def get_all_transactions():
    return session.query(Transaction).all()
