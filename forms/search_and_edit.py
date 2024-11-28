import streamlit as st
from utils.filter_df_date import filter_df_date
from database.db_handler import get_Transactions_Dataframe, get_transaction, delete_transaction
from forms.edit_register import render_formulario_edicao


def render_transactions_as_cards(df):
    for index, row in df.iterrows():
        with st.container():
            # Create columns 
            col1, col2, col3, col4 = st.columns([1, 2, 1, 1])

            # Display the ID and date in the first column
            col1.markdown(f"**ID:** {row['ID']}")
            col1.markdown(f"**Data:** {row['Data'].strftime('%d/%m/%Y')}")

            # Display the description and type in the second column
            col2.markdown(f"**Descrição:** {row['Descrição']}")
            col2.markdown(f"**Tipo:** {row['Tipo']}")
            col2.markdown(f"**Valor:** R$ {row['Valor']:.2f}")

            # Display categories in the third column
            col3.markdown(f"**Categorias:** {row['Categorias']}")

            # Add buttons for Edit and Delete in the fourth column
            edit_button = col4.checkbox("✏️ Editar", key=f"edit_{row['ID']}")
            delete_button = col4.checkbox("🗑️ Excluir", key=f"delete_{row['ID']}")

            st.markdown("---")

            if edit_button:
                selected_transaction = get_transaction(row['ID'])

                render_formulario_edicao(selected_transaction)

            # Botão inicial para deletar
            if delete_button:
                # Exibe uma mensagem de confirmação
                st.warning(f"Tem certeza que deseja deletar a transação ID {row['ID']}?")
                
                col1, col2 = st.columns(2)
                # Botão de confirmação final
                confirm_delete = col1.button('Sim, deletar ✅', key=f"confirm_delete_{row['ID']}")
                cancel_delete = col2.button('Cancelar ❌', key=f"cancel_delete_{row['ID']}")

                if confirm_delete:
                    try:
                        delete_transaction(row['ID'])
                        st.success(f"✅ Transação ID {row['ID']} excluída com sucesso!")
                    except Exception as e:
                        st.error(f"❌ Não foi possível excluir a transação: {e}")
                
                if cancel_delete:
                    st.info("A exclusão da transação foi cancelada.")


def search_all_columns(df, search_term):
    return df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False, na=False).any(), axis=1)]

# search, display, edit, and delete
def search_and_edit_transactions():
    
    df_transactions = get_Transactions_Dataframe()
    
    if df_transactions.empty:
        st.write("Nenhuma transação encontrada.")
    else:
        # Use the filter_df_date function to filter by date
        df_filtered = filter_df_date(df_transactions)
        st.divider()
        st.subheader("🔍 Pesquisar")
        # Search bar to filter across all columns
        search_term = st.text_input("Pesquisar por termo")

        if search_term:
            df_filtered = search_all_columns(df_filtered, search_term)

        # Filter by transaction type (CREDITO or DEBITO)
        tipo_transacao = st.radio("Filtrar por Tipo de Transação", options=["Todas", "Receita (Crédito)", "Despesa (Débito)"])

        if tipo_transacao == "Receita (Crédito)":
            df_filtered = df_filtered[df_filtered['Tipo'] == "Receita"]
        elif tipo_transacao == "Despesa (Débito)":
            df_filtered = df_filtered[df_filtered['Tipo'] == "Despesa"]

        if df_filtered.empty:
            st.write("Nenhuma transação encontrada.")
        else:
            # Inform how many transactions were found
            st.write(f"**{len(df_filtered)}** transações encontradas:")
            st.divider()
            # Render transactions as cards with Edit and Delete buttons
            render_transactions_as_cards(df_filtered)

# Running the search and edit functionality
if __name__ == "__main__":
    search_and_edit_transactions()
