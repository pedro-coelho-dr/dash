import streamlit as st
import pandas as pd
from database.db_handler import get_all_transactions, TransactionTypeEnum

def overview():
    st.title("💸 Visão Geral do Fluxo de Caixa")
    
    # Buscar transações do banco de dados
    transactions = get_all_transactions()
    
    if transactions:
        # Converter registros de transações para um DataFrame do Pandas
        transaction_data = {
            "Data": [t.date for t in transactions],
            "Descrição": [t.description for t in transactions],
            "Valor": [t.value for t in transactions],
            "Tipo": ["Receita" if t.type == TransactionTypeEnum.CREDITO else "Despesa" for t in transactions],
            "Categorias": [", ".join([cat.name for cat in t.categories]) for t in transactions]  # Adiciona categorias
        }
        df_transactions = pd.DataFrame(transaction_data)

        # Exibir DataFrame como uma tabela
        st.subheader("📋 Transações Recentes")
        st.table(df_transactions)

        # Calcular total de receitas e despesas
        total_receitas = df_transactions[df_transactions["Tipo"] == "Receita"]["Valor"].sum()
        total_despesas = df_transactions[df_transactions["Tipo"] == "Despesa"]["Valor"].sum()
        saldo_liquido = total_receitas - total_despesas

        # Exibir KPIs com ícones e cores
        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Total de Receitas", f"R$ {total_receitas:,.2f}", delta=f"+R$ {total_receitas:,.2f}", delta_color="normal")
        col2.metric("💸 Total de Despesas", f"R$ {total_despesas:,.2f}", delta=f"-R$ {total_despesas:,.2f}", delta_color="inverse")
        col3.metric("🧾 Saldo Líquido", f"R$ {saldo_liquido:,.2f}")

        # Exibir gráfico de barras com receitas e despesas
        st.subheader("📊 Gráfico de Receitas e Despesas")
        df_summary = pd.DataFrame({
            "Tipo": ["Receita", "Despesa"],
            "Valor": [total_receitas, total_despesas]
        })
        st.bar_chart(df_summary.set_index("Tipo"))

    else:
        st.write("Nenhuma transação encontrada.")

# Executando a função
if __name__ == "__main__":
    overview()
