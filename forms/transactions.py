import streamlit as st
from forms.insert_revenue import render_form as render_revenue_form
from forms.insert_expense import render_form as render_expense_form
from forms.search_and_edit import search_and_edit_transactions

# Function to render the transaction page
def render_transaction_page():
    st.title("💼 Transações")

    # Buttons to switch between different transaction options
    selected_form = st.radio(
        "Escolha o tipo de ação:", 
        ('Gerenciar Transações', 'Inserir Receita', 'Inserir Despesa'),
        index=0
    )

    # Render the appropriate form based on selection
    if selected_form == 'Inserir Receita':
        st.header("💰 Inserir Receita")
        render_revenue_form()

    elif selected_form == 'Inserir Despesa':
        st.header("💸 Inserir Despesa")
        render_expense_form()

    elif selected_form == 'Gerenciar Transações':
        st.header("🔍 Gerenciar Transações")
        search_and_edit_transactions()

# Executing the transaction page
if __name__ == "__main__":
    render_transaction_page()
