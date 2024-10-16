import streamlit as st
from utils.filter_df_date import filter_df_date
from database.db_handler import get_Transactions_Dataframe, get_transaction, delete_transaction
from forms.edit_register import render_formulario_edicao

# Function to search, display, edit, and delete transactions
def search_and_edit_transactions():
    df_transactions = get_Transactions_Dataframe()

    if df_transactions.empty:
        st.write("Nenhuma transação encontrada.")
    else:
        # Use the filter_df_date function to filter by date
        df_filtered = filter_df_date(df_transactions)

        # Search bar to filter by description
        search_term = st.text_input("Pesquisar por descrição:")

        if search_term:
            df_filtered = df_filtered[df_filtered['Descrição'].str.contains(search_term, case=False, na=False)]

        if df_filtered.empty:
            st.write("Nenhuma transação encontrada.")
        else:
            # Automatically render the filtered transactions in a table
            st.write(f"Encontradas {len(df_filtered)} transações:")
            st.dataframe(df_filtered, use_container_width=True)

            # Let the user select a transaction to edit or delete
            transaction_id = st.selectbox("Selecione a Transação para Editar ou Excluir:", df_filtered.index)
            selected_transaction = df_filtered.loc[transaction_id]

            # Display and edit the selected transaction
            st.write("### Detalhes da Transação")
            st.write(f"**Data:** {selected_transaction['Data']}")
            st.write(f"**Descrição:** {selected_transaction['Descrição']}")
            st.write(f"**Valor:** R$ {selected_transaction['Valor']}")
            st.write(f"**Tipo:** {selected_transaction['Tipo']}")
            st.write(f"**Categorias:** {selected_transaction['Categorias']}")

            # Render the form for editing
            render_formulario_edicao(get_transaction(transaction_id))

            # Button to delete the transaction
            if st.button("🗑️ Excluir Transação"):
                try:
                    delete_transaction(transaction_id)
                    st.success("✅ Transação excluída com sucesso!")
                    st.experimental_rerun()  # Reload the page after deletion
                except Exception as e:
                    st.error(f"❌ Não foi possível excluir a transação: {e}")

# Running the search and edit functionality
if __name__ == "__main__":
    search_and_edit_transactions()
