import streamlit as st
import pandas as pd
import plotly.express as px
from database.db_handler import Transaction, get_Transactions_Dataframe, update_transaction


def overview():
    st.title("💸 Visão Geral do Fluxo de Caixa")

    # Carregar as transações do banco de dados
    df_transactions = get_Transactions_Dataframe()

    if not df_transactions.empty:
        # Normalizar dados
        df_transactions = df_transactions.sort_values(by="Data", ascending=False)  # Ordena pela coluna 'Data'

        # Exibir DataFrame como uma tabela
        st.subheader("📋 Transações Recentes")
        show_all = st.checkbox("Mostrar Todas as Entradas", value=False)

        # Exibe todas as transações em uma tabela scrollável
        if show_all:
            st.dataframe(df_transactions, use_container_width=True)  
        else:
            st.dataframe(df_transactions.head(30), use_container_width=True)  # Exibe apenas as primeiras 30 transações

        # Calcular total de receitas e despesas
        total_receitas = df_transactions[df_transactions["Tipo"] == "Receita"]["Valor"].sum()
        total_despesas = df_transactions[df_transactions["Tipo"] == "Despesa"]["Valor"].sum()
        saldo_liquido = total_receitas - total_despesas

        # Exibir KPIs com ícones e cores
        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Total de Receitas", f"R$ {total_receitas:,.2f}", delta=f"+R$ {total_receitas:,.2f}", delta_color="normal")
        col2.metric("💸 Total de Despesas", f"R$ {total_despesas:,.2f}", delta=f"-R$ {total_despesas:,.2f}", delta_color="normal")
        col3.metric("🧾 Saldo Líquido", f"R$ {saldo_liquido:,.2f}")

        # Exibir gráfico de barras interativo com receitas e despesas ao longo do tempo
        st.subheader("📊 Gráfico Interativo de Receitas e Despesas")
        df_summary = df_transactions.groupby(['Data', 'Tipo']).sum().reset_index()  # Agrupar por Data e Tipo

        # Criar gráfico de barras
        fig = px.bar(df_summary, x='Data', y='Valor', color='Tipo', barmode='group',
                     title='Receitas e Despesas ao Longo do Tempo',
                     labels={'Valor': 'Valor (R$)', 'Data': 'Data'},
                     template='plotly_white',
                     color_discrete_map={"Receita": "#09AB3B", "Despesa": "#FF2B2B"})  # Especificar as cores

        st.plotly_chart(fig)

        # Seção para selecionar e editar transações
        st.subheader("✏️ Editar Transação")
        transaction_id = st.selectbox("Selecione a Transação para Editar:", df_transactions.index)
        selected_transaction = df_transactions.loc[transaction_id]

        # Exibir detalhes da transação selecionada
        st.write("### Detalhes da Transação")
        st.write(f"**Data:** {selected_transaction['Data']}")
        st.write(f"**Descrição:** {selected_transaction['Descrição']}")
        st.write(f"**Valor:** R$ {selected_transaction['Valor']}")
        st.write(f"**Tipo:** {selected_transaction['Tipo']}")
        st.write(f"**Categorias:** {selected_transaction['Categorias']}")

        # Formulário para editar a transação
        with st.form(key='edit_form'):
            new_date = d
            new_description = st.text_input("Descrição", value=selected_transaction['Descrição'])
            new_value = st.number_input("Valor", value=selected_transaction['Valor'])
            new_type = st.selectbox("Tipo", options=["Receita", "Despesa"], index=["Receita", "Despesa"].index(selected_transaction['Tipo']))
            new_categories = st.text_input("Categorias (separadas por vírgula)", value=selected_transaction['Categorias'])

            Transaction()

            # Botão para salvar alterações
            submitted = st.form_submit_button("Salvar Alterações")

            if submitted:
                # Atualizar a transação no DataFrame (ou no banco de dados)
                df_transactions.at[transaction_id, 'Descrição'] = new_description
                df_transactions.at[transaction_id, 'Valor'] = new_value
                df_transactions.at[transaction_id, 'Tipo'] = new_type
                df_transactions.at[transaction_id, 'Categorias'] = new_categories

                # Chame a função para atualizar no banco de dados (exemplo)
                update_transaction(transaction_id, new_description, new_value, new_type, new_categories)

                st.success("Transação atualizada com sucesso!")

    else:
        st.write("Nenhuma transação encontrada.")

# Executando a função
if __name__ == "__main__":
    overview()
