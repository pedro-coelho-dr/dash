import streamlit as st
import pandas as pd
from database.db_handler import get_all_transactions

def overview():
    st.title("Visão Geral do Fluxo de Caixa")
    
    # Fetch transactions from the database
    transactions = get_all_transactions()
    
    # If there are transactions, process them
    if transactions:
        # Convert the transaction records to a pandas DataFrame
        transaction_data = {
            "Data": [t.date for t in transactions],
            "Descrição": [t.description for t in transactions],
            "Valor": [t.value for t in transactions],
            "Tipo": [t.type for t in transactions]
        }
        df_transactions = pd.DataFrame(transaction_data)

        # Display the DataFrame as a table
        st.subheader("Transações Recentes")
        st.table(df_transactions)

        # Calculate total income and expenses
        total_receitas = df_transactions[df_transactions["Tipo"] == "Receita"]["Valor"].sum()
        total_despesas = df_transactions[df_transactions["Tipo"] == "Despesa"]["Valor"].sum()
        saldo_liquido = total_receitas - total_despesas

        # Display KPIs
        st.metric("Total de Receitas", f"R$ {total_receitas}")
        st.metric("Total de Despesas", f"R$ {total_despesas}")
        st.metric("Saldo Líquido", f"R$ {saldo_liquido}")

    else:
        st.write("Nenhuma transação encontrada.")
