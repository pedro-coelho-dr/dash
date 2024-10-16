import streamlit as st
from forms import transactions 
from analysis import overview, advanced_analysis

# Sidebar menu for navigation
st.sidebar.title("Menu Principal")
menu_option = st.sidebar.radio(
    "Selecione uma opção:", 
    ["Visão Geral", "Análise Avançada", "Transações"]
)

# Display sections based on the menu choice
if menu_option == "Visão Geral":
    overview.overview()

elif menu_option == "Análise Avançada":
    advanced_analysis.advanced_analysis()

elif menu_option == "Transações":
    transactions.render_transaction_page()
