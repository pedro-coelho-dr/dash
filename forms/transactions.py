import streamlit as st
from forms.insert_revenue import render_form as render_revenue_form
from forms.insert_expense import render_form as render_expense_form

# Function to render the transaction page
def render_transaction_page():
    st.title("💼 Transações")

    # Buttons to switch between Receita and Despesa forms
    selected_form = st.radio(
        "Escolha o tipo de transação:", 
        ('Receita', 'Despesa'),
        index=0
    )

    # Render the appropriate form based on selection
    if selected_form == 'Receita':
        st.header("💰 Inserir Receita")
        render_revenue_form()
    elif selected_form == 'Despesa':
        st.header("💸 Inserir Despesa")
        render_expense_form()

# Executing the transaction page
if __name__ == "__main__":
    render_transaction_page()
