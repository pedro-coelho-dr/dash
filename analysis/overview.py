from datetime import timedelta
import streamlit as st
import pandas as pd
import plotly.express as px
from database.db_handler import get_Transactions_Dataframe, get_transaction
from forms.edit_register import render_formulario_edicao

def overview():
    st.title("💸 Visão Geral")

    # Carregar as transações do banco de dados
    df_transactions = get_Transactions_Dataframe()

    if not df_transactions.empty:
        # Normalizar dados
        df_transactions['Data'] = pd.to_datetime(df_transactions['Data'])  # Certificar que 'Data' está no formato datetime
        df_transactions = df_transactions.sort_values(by="Data", ascending=False)  # Ordena pela coluna 'Data'

        # Filtrar periodo de analise
        st.subheader("📅 Filtrar por Período")
        # Checkbox para ativar filtro customizado
        if st.checkbox("Usar filtro personalizado de período"):
            # Seção de filtro por período
            col1, col2 = st.columns(2)
            start_date = col1.date_input("Data de Início", df_transactions['Data'].max().date() - timedelta(days=30))
            end_date = col2.date_input("Data de Fim", df_transactions['Data'].max().date())

            # Filtrar o DataFrame pelas datas selecionadas
            df_filtered = df_transactions[(df_transactions['Data'] >= pd.to_datetime(start_date)) & 
                                        (df_transactions['Data'] <= pd.to_datetime(end_date))]
        else:

            # Adicionar colunas de ano e mês para facilitar o filtro
            df_transactions['Ano'] = df_transactions['Data'].dt.year
            df_transactions['Mês'] = df_transactions['Data'].dt.month

            # Filtro por ano e mês
            col1, col2 = st.columns(2)
           # Obter o último ano e mês a partir dos dados
            last_year = df_transactions['Ano'].max()
            last_month = df_transactions[df_transactions['Ano'] == last_year]['Mês'].max()

            # Seleção do ano com o último ano como padrão
            selected_year = col1.selectbox("Selecione o Ano", 
                                        options=sorted(df_transactions['Ano'].unique(), reverse=True),
                                        index=sorted(df_transactions['Ano'].unique(), reverse=True).index(last_year))

            # Seleção do mês com o último mês como padrão
            selected_month = col2.selectbox("Selecione o Mês", 
                                            options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                            format_func=lambda x: pd.to_datetime(f'2024-{x:02d}-01').strftime('%B'),
                                            index=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12].index(last_month))

            # Filtrar o DataFrame com base no mês e ano selecionados
            df_filtered = df_transactions[(df_transactions['Ano'] == selected_year) & (df_transactions['Mês'] == selected_month)]



        # Calcular total de receitas e despesas
        total_receitas = df_filtered[df_filtered["Tipo"] == "Receita"]["Valor"].sum()
        total_despesas = df_filtered[df_filtered["Tipo"] == "Despesa"]["Valor"].sum()
        saldo_liquido = total_receitas - total_despesas

        # Mostrar Métricas
        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Total de Receitas", f"R$ {total_receitas:,.2f}", delta=f"+R$ {total_receitas:,.2f}", delta_color="normal")
        col2.metric("💸 Total de Despesas", f"R$ {total_despesas:,.2f}", delta=f"-R$ {total_despesas:,.2f}", delta_color="normal")
        col3.metric("🧾 Saldo Líquido", f"R$ {saldo_liquido:,.2f}")

        df_summary = df_filtered.groupby(['Data', 'Tipo']).sum().reset_index()
        
        # # Gráfico de barras
        # fig = px.bar(df_summary, x='Data', y='Valor', color='Tipo', barmode='group',
        #              title='Receitas e Despesas ao Longo do Tempo',
        #              labels={'Valor': 'Valor (R$)', 'Data': 'Data'},
        #              template='plotly_white',
        #              color_discrete_map={"Receita": "#09AB3B", "Despesa": "#FF2B2B"})
        # st.plotly_chart(fig)

        # Gráfico de linha
        fig = px.line(df_summary, x='Data', y='Valor', color='Tipo',
                      title='Receitas e Despesas ao Longo do Tempo',
                      labels={'Valor': 'Valor (R$)', 'Data': 'Data'},
                      template='plotly_white',
                      color_discrete_map={"Receita": "#09AB3B", "Despesa": "#FF2B2B"})
        st.plotly_chart(fig)

        # Donut chart for Métodos de Pagamento
        if 'Método de Pagamento' in df_filtered.columns:
            payment_method_counts = df_filtered['Método de Pagamento'].value_counts().reset_index()
            payment_method_counts.columns = ['Método de Pagamento', 'Contagem']  # Rename columns

            # Create donut chart for payment methods
            fig_payment_methods = px.pie(payment_method_counts, values='Contagem', names='Método de Pagamento', 
                                        title='Métodos de Pagamento', 
                                        hole=0.4,  # More pronounced donut hole
                                        template='plotly_dark')  # Use a dark theme

            fig_payment_methods.update_traces(textinfo='percent+label', hoverinfo='label+percent+value')

            st.plotly_chart(fig_payment_methods)
        else:
            st.write("Nenhuma informação de métodos de pagamento disponível.")

        # Donut chart for Bancos
        if 'Banco' in df_filtered.columns:
            bank_counts = df_filtered['Banco'].value_counts().reset_index()
            bank_counts.columns = ['Banco', 'Contagem']  # Rename columns

            # Create donut chart for banks
            fig_banks = px.pie(bank_counts, values='Contagem', names='Banco', 
                            title='Bancos', 
                            hole=0.4,
                            template='plotly_dark')  # Use a dark theme

            fig_banks.update_traces(textinfo='percent+label', hoverinfo='label+percent+value')

            st.plotly_chart(fig_banks)
        else:
            st.write("Nenhuma informação de bancos disponível.")

        # Exibir DataFrame como uma tabela
        st.subheader("📋 Transações Recentes")
        show_all = st.checkbox("Mostrar Todas as Entradas", value=False)

        if show_all:
            st.dataframe(df_filtered, use_container_width=True)
        else:
            st.dataframe(df_filtered.head(30), use_container_width=True)

        # Seção para selecionar e editar transações
        if st.checkbox("✏️ Editar Transação", value=False):
            transaction_id = st.selectbox("Selecione a Transação para Editar:", df_filtered.index)
            selected_transaction = df_filtered.loc[transaction_id]

            st.write("### Detalhes da Transação")
            st.write(f"**Data:** {selected_transaction['Data']}")
            st.write(f"**Descrição:** {selected_transaction['Descrição']}")
            st.write(f"**Valor:** R$ {selected_transaction['Valor']}")
            st.write(f"**Tipo:** {selected_transaction['Tipo']}")
            st.write(f"**Categorias:** {selected_transaction['Categorias']}")

            render_formulario_edicao(get_transaction(transaction_id))

    else:
        st.write("Nenhuma transação encontrada.")

# Executando a função
if __name__ == "__main__":
    overview()
