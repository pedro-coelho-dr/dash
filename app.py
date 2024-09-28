import streamlit as st
from forms import insert_revenue, insert_expense  
from analysis import overview, advanced_analysis

# Sidebar menu for navigation
st.sidebar.title("Menu Principal")
menu_option = st.sidebar.radio(
    "Selecione uma opção:", 
    ["Visão Geral", "Análise Avançada", "Inserir Receita", "Inserir Despesa"]
)

# Display sections based on the menu choice
if menu_option == "Visão Geral":
    overview.overview()

elif menu_option == "Análise Avançada":
    advanced_analysis.advanced_analysis()

elif menu_option == "Inserir Receita":
    st.title("Inserir Receita")
    insert_revenue.render_form()

elif menu_option == "Inserir Despesa":
    st.title("Inserir Despesa")
    insert_expense.render_form()
