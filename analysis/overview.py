import streamlit as st
import pandas as pd
from database.db_handler import get_all_transactions, TransactionTypeEnum

def overview():
    st.title("💸 Visão Geral do Fluxo de Caixa")
    
    # Buscar transações do banco de dados
    transactions = get_all_transactions()
    
    # Converter registros de transações para um DataFrame do Pandas
    if transactions:

        transaction_data = {
            "Data": [],
            "Descrição": [],
            "Valor": [],
            "Tipo": [],
            "Categorias": []  # categorias como strings ["cat1, cat2", "cat2", "cat1, cat3", ...]
        }
        
        # Armazenar todas as transações no dicionário por coluna
        for t in transactions:
            transaction_data["Data"].append(t.date)
            transaction_data["Descrição"].append(t.description)
            transaction_data["Valor"].append(t.value)
            transaction_data["Tipo"].append("Receita" if t.type == TransactionTypeEnum.CREDITO.name else "Despesa")
            transaction_data["Categorias"].append(", ".join([cat.name for cat in t.categories]))

        # Criar DataFrame com dicionário
        df_transactions = pd.DataFrame(transaction_data)

        # Normalizar dados
        df_transactions = df_transactions.sort_values(by="Data", ascending=False)  # Ordena pela coluna 'Data'

        # Exibir DataFrame como uma tabela
        st.subheader("📋 Transações Recentes")
        show_all = st.checkbox("Mostrar Todas as Entradas", value=False)


        # Exibe todas as transações em uma tabela scrollável
        if show_all:
            st.dataframe(df_transactions, use_container_width=True)  
        else:
            st.dataframe(df_transactions.head(30), use_container_width=True)  # Exibe apenas as primeiras 30 transações em uma tabela scrollável

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
