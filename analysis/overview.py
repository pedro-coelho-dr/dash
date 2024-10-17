from datetime import timedelta
import streamlit as st
import pandas as pd
import plotly.express as px
from database.db_handler import get_Transactions_Dataframe, get_transaction
from utils.filter_df_date import filter_df_date
from utils.balance_histogram import balance_histogram
from utils.income_outcome_area import income_outcome_area

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
        income_outcome_area(df_summary)

        # Gráfico de saldo histórico
        st.subheader("📊 Histórico de Saldo")
        balance_histogram(df_summary)


        col1, col2 = st.columns(2)

        # Donut chart for Métodos de Pagamento
        if 'Método de Pagamento' in df_filtered.columns:
            col1.subheader("💳 Métodos de Pagamento")
            payment_method_counts = df_filtered['Método de Pagamento'].value_counts().reset_index()
            payment_method_counts.columns = ['Método de Pagamento', 'Contagem']  # Rename columns

            # Define a custom color palette
            color_palette = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880']

            fig_payment_methods = px.pie(payment_method_counts, values='Contagem', names='Método de Pagamento',
                                        hole=0.5,  # More pronounced donut hole
                                        color_discrete_sequence=color_palette,  # Custom colors
                                        template='plotly_dark')  # Use a dark theme

            # Enhance labels and hover info
            fig_payment_methods.update_traces(textinfo='percent+label', hoverinfo='label+percent+value', 
                                            marker=dict(line=dict(color='#000000', width=2)))  # Add border to slices
            fig_payment_methods.update_layout(annotations=[dict(text='Métodos', x=0.5, y=0.5, font_size=20, showarrow=False)])

            col1.plotly_chart(fig_payment_methods)

        else:
            col1.write("Nenhuma informação de métodos de pagamento disponível.")

        # Donut chart for Bancos
        if 'Banco' in df_filtered.columns:
            col2.subheader("🏦 Bancos Utilizados")
            bank_counts = df_filtered['Banco'].value_counts().reset_index()
            bank_counts.columns = ['Banco', 'Contagem']  # Rename columns

            # Define a custom color palette
            color_palette_banks = ['#FF7F0E', '#2CA02C', '#D62728', '#9467BD', '#8C564B', '#E377C2', '#7F7F7F', '#BCBD22']

            fig_banks = px.pie(bank_counts, values='Contagem', names='Banco', 
                            hole=0.5,  # Donut chart
                            color_discrete_sequence=color_palette_banks,  # Custom colors
                            template='plotly_dark')

            # Enhance labels and hover info
            fig_banks.update_traces(textinfo='percent+label', hoverinfo='label+percent+value', 
                                    marker=dict(line=dict(color='#000000', width=2)))  # Add border to slices
            fig_banks.update_layout(annotations=[dict(text='Bancos', x=0.5, y=0.5, font_size=20, showarrow=False)])

            col2.plotly_chart(fig_banks)

        else:
            col2.write("Nenhuma informação de bancos disponível.")


    else:
        st.write("Nenhuma transação encontrada.")

# Executando a função
if __name__ == "__main__":
    overview()
