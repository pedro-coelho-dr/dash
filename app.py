import streamlit as st
from forms import transactions 
from analysis import overview, advanced_analysis, predictions

# Set the page configuration
st.set_page_config(
    page_title="Xero",  # Title in the browser tab
    page_icon="⭐",  # Cloud icon (you can replace with a URL to a custom icon)
    layout="wide",  # Wide layout for better use of space
    initial_sidebar_state="expanded"  # Sidebar starts expanded
)
st.markdown(
    """
    <style>
    /* Centralize the sidebar image */
    [data-testid="stSidebar"] img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 50%; /* Adjust the width as needed */
    }
    </style>
    """,
    unsafe_allow_html=True
)

LOGO_URL = "static/logo.png"
st.sidebar.image(
    LOGO_URL,
    use_column_width=False  # Automatically adjust the image to fit the sidebar width
)
# Sidebar menu for navigation
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
