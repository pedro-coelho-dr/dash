import streamlit as st
from forms import transactions 
from analysis import overview, advanced_analysis, predictions

# Set the page configuration
st.set_page_config(
    page_title="Dash",  # Title in the browser tab
    page_icon="⭐",  # Cloud icon (you can replace with a URL to a custom icon)
    layout="wide",  # Wide layout for better use of space
    initial_sidebar_state="expanded"  # Sidebar starts expanded
)


# Sidebar menu for navigation
st.sidebar.title("Dash")
menu_option = st.sidebar.radio(
    ">>", 
    ["Visão Geral", "Análise Avançada", "Previsões", "Transações"]
)

# Display sections based on the menu choice
if menu_option == "Visão Geral":
    overview.overview()

elif menu_option == "Análise Avançada":
    advanced_analysis.advanced_analysis()

elif menu_option == "Transações":
    transactions.render_transaction_page()

elif menu_option == "Previsões":
    predictions.render_predictions_page()
