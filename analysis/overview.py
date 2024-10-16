from datetime import timedelta
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.balance_histogram import balance_histogram
from database.db_handler import get_Transactions_Dataframe, get_transaction
from forms.edit_register import render_formulario_edicao
from utils.filter_df_date import filter_df_date

def overview():
    st.title("💸 Visão Geral")

    # Carregar as transações do banco de dados
    df_transactions = get_Transactions_Dataframe()

    if not df_transactions.empty:
        # Normalizar dados
        df_transactions['Data'] = pd.to_datetime(df_transactions['Data'])  # Certificar que 'Data' está no formato datetime
        df_transactions = df_transactions.sort_values(by="Data", ascending=False)  # Ordena pela coluna 'Data'

        # filtrar dataframe por data
        df_filtered = filter_df_date(df_transactions)

        # Calcular total de receitas e despesas
        total_receitas = df_filtered[df_filtered["Tipo"] == "Receita"]["Valor"].sum()
        total_despesas = df_filtered[df_filtered["Tipo"] == "Despesa"]["Valor"].sum()
        saldo_liquido = total_receitas - total_despesas

        # Adicionar título para a seção de métricas
        st.subheader("📊 Resumo Financeiro")

        # Mostrar Métricas
        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Total de Receitas", f"R$ {total_receitas:,.2f}", delta=f"+R$ {total_receitas:,.2f}", delta_color="normal")
        col2.metric("💸 Total de Despesas", f"R$ {total_despesas:,.2f}", delta=f"-R$ {total_despesas:,.2f}", delta_color="normal")
        col3.metric("🧾 Saldo Líquido", f"R$ {saldo_liquido:,.2f}")

        df_summary = df_filtered.groupby(['Data', 'Tipo']).sum().reset_index()

        # Gráfico de linha (Receitas e Despesas ao longo do tempo)
        st.subheader("📈 Receitas e Despesas ao Longo do Tempo")
        fig = px.line(df_summary, x='Data', y='Valor', color='Tipo',
                      labels={'Valor': 'Valor (R$)', 'Data': 'Data'},
                      template='plotly_white',
                      color_discrete_map={"Receita": "#09AB3B", "Despesa": "#FF2B2B"})
        st.plotly_chart(fig)

        # Gráfico de saldo histórico
        st.subheader("📊 Histórico de Saldo")
        balance_histogram(df_summary)

        # Donut chart for Métodos de Pagamento
        if 'Método de Pagamento' in df_filtered.columns:
            st.subheader("💳 Métodos de Pagamento")
            payment_method_counts = df_filtered['Método de Pagamento'].value_counts().reset_index()
            payment_method_counts.columns = ['Método de Pagamento', 'Contagem']  # Rename columns

            fig_payment_methods = px.pie(payment_method_counts, values='Contagem', names='Método de Pagamento', 
                                        hole=0.4,  # More pronounced donut hole
                                        template='plotly_dark')  # Use a dark theme
            fig_payment_methods.update_traces(textinfo='percent+label', hoverinfo='label+percent+value')

            st.plotly_chart(fig_payment_methods)
        else:
            st.write("Nenhuma informação de métodos de pagamento disponível.")

        # Donut chart for Bancos
        if 'Banco' in df_filtered.columns:
            st.subheader("🏦 Bancos Utilizados")
            bank_counts = df_filtered['Banco'].value_counts().reset_index()
            bank_counts.columns = ['Banco', 'Contagem']  # Rename columns

            fig_banks = px.pie(bank_counts, values='Contagem', names='Banco', 
                            hole=0.4,
                            template='plotly_dark')  # Use a dark theme
            fig_banks.update_traces(textinfo='percent+label', hoverinfo='label+percent+value')

            st.plotly_chart(fig_banks)
        else:
            st.write("Nenhuma informação de bancos disponível.")
    else:
        st.write("Nenhuma transação encontrada.")

# Executando a função
if __name__ == "__main__":
    overview()
