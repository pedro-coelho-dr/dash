from datetime import timedelta
import streamlit as st
import pandas as pd
import plotly.express as px
from database.db_handler import get_Transactions_Dataframe, get_transaction
from utils.filter_df_date import filter_df_date
from utils.balance_histogram import balance_histogram
from utils.income_outcome_area import income_outcome_area

def overview():
    st.title("Visão Geral")

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
            st.subheader("💳 Métodos de Pagamento")
            payment_method_counts = df_filtered['Método de Pagamento'].value_counts().reset_index()
            payment_method_counts.columns = ['Método de Pagamento', 'Contagem']  # Rename columns

            # Custom color palette with 4 different tones
            color_palette = ['#1565C0', '#FFC107', '#00CC96', '#AB63FA']

            fig_payment_methods = px.pie(
                payment_method_counts,
                values='Contagem',
                names='Método de Pagamento',
                hole=0.4,  # Donut chart style
                color_discrete_sequence=color_palette,  # Use the custom palette
                template='plotly_dark'  # Dark theme for modern appearance
            )

            # Enhance labels and hover info
            fig_payment_methods.update_traces(
                textinfo='percent+label',
                hoverinfo='label+percent+value',
                marker=dict(line=dict(color='#FFFFFF', width=1.5))  # Add white border
            )
            fig_payment_methods.update_layout(
                annotations=[dict(
                    text='Métodos',
                    x=0.5, y=0.5,
                    font_size=18,
                    font_family="Arial",
                    showarrow=False
                )],
                font=dict(family="Arial", size=12, color="#E1E1E1")  # Update font to light gray
            )

            st.plotly_chart(fig_payment_methods, use_container_width=True)

        else:
            st.write("Nenhuma informação de métodos de pagamento disponível.")

        # Donut chart for Bancos
        if 'Banco' in df_filtered.columns:
            st.subheader("🏦 Bancos Utilizados")
            bank_counts = df_filtered['Banco'].value_counts().reset_index()
            bank_counts.columns = ['Banco', 'Contagem']  # Rename columns

            # Custom color palette with 4 different tones
            color_palette_banks = ['#1565C0', '#FFC107', '#00CC96', '#AB63FA']

            fig_banks = px.pie(
                bank_counts,
                values='Contagem',
                names='Banco',
                hole=0.4,  # Donut chart style
                color_discrete_sequence=color_palette_banks,  # Use the custom palette
                template='plotly_dark'
            )

            # Enhance labels and hover info
            fig_banks.update_traces(
                textinfo='percent+label',
                hoverinfo='label+percent+value',
                marker=dict(line=dict(color='#FFFFFF', width=1.5))  # Add white border
            )
            fig_banks.update_layout(
                annotations=[dict(
                    text='Bancos',
                    x=0.5, y=0.5,
                    font_size=18,
                    font_family="Arial",
                    showarrow=False
                )],
                font=dict(family="Arial", size=12, color="#E1E1E1")
            )

            st.plotly_chart(fig_banks, use_container_width=True)

        else:
            st.write("Nenhuma informação de bancos disponível.")


    else:
        st.write("Nenhuma transação encontrada.")

# Executando a função
if __name__ == "__main__":
    overview()
