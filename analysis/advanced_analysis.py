import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import altair as alt
from sqlalchemy import create_engine
from database.db_handler import get_all_transactions

# Function to load transactions from the database and return them as a pandas DataFrame
def load_transactions():
    # Fetch transactions from the database
    transactions = get_all_transactions()

    # Convert to a pandas DataFrame for easy manipulation
    data = {
        'date': [t.date for t in transactions],
        'type': [t.type for t in transactions],
        'value': [t.value for t in transactions],
        'category': [t.category for t in transactions],
        'description': [t.description for t in transactions],
    }

    return pd.DataFrame(data)

# Function for generating bar charts
def plot_bar_chart(df):
    st.subheader("Bar Chart: Total by Category")
    bar_data = df.groupby('category')['value'].sum()
    st.bar_chart(bar_data)

# Function for generating line charts
def plot_line_chart(df):
    st.subheader("Line Chart: Value Over Time")
    df_sorted = df.sort_values(by='date')
    st.line_chart(df_sorted.set_index('date')['value'])

# Function for generating area charts
def plot_area_chart(df):
    st.subheader("Area Chart: Cumulative Value Over Time")
    df_sorted = df.sort_values(by='date')
    df_sorted['cumulative_value'] = df_sorted['value'].cumsum()
    st.area_chart(df_sorted.set_index('date')['cumulative_value'])

# Function for generating scatter plots
def plot_scatter_chart(df):
    st.subheader("Scatter Plot: Value by Category")
    fig = px.scatter(df, x='category', y='value', color='type', size='value',
                     title='Scatter Plot of Transaction Value by Category')
    st.plotly_chart(fig)

# Advanced Analysis section
def advanced_analysis():
    st.title("Análise Avançada - Comparação de Categorias")

    # Load transactions from the database
    df = load_transactions()

    if not df.empty:
        # Display different charts
        plot_bar_chart(df)
        plot_line_chart(df)
        plot_area_chart(df)
        plot_scatter_chart(df)

    else:
        st.write("No data available.")

# Running the advanced analysis
if __name__ == '__main__':
    advanced_analysis()
