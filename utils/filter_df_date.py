import pandas as pd
import streamlit as st
from datetime import timedelta

def filter_df_date(df):
    st.subheader("📅 Filtrar por Período")

    # Ensure the 'Data' column is in datetime format
    df['Data'] = pd.to_datetime(df['Data'], errors='coerce')

    # Checkbox to activate custom period filter
    if st.checkbox("Usar filtro personalizado de período"):
        col1, col2 = st.columns(2)
        start_date = col1.date_input("Data de Início", df['Data'].max().date() - timedelta(days=30))
        end_date = col2.date_input("Data de Fim", df['Data'].max().date())

        # Filter the DataFrame by the selected dates
        df_filtered = df[(df['Data'] >= pd.to_datetime(start_date)) & (df['Data'] <= pd.to_datetime(end_date))]
    else:
        # Add 'Ano' and 'Mês' columns to facilitate filtering
        df['Ano'] = df['Data'].dt.year
        df['Mês'] = df['Data'].dt.month

        col1, col2 = st.columns(2)
        last_year = df['Ano'].max()
        last_month = df[df['Ano'] == last_year]['Mês'].max()

        selected_year = col1.selectbox("Selecione o Ano", 
                                       options=sorted(df['Ano'].unique(), reverse=True),
                                       index=sorted(df['Ano'].unique(), reverse=True).index(last_year))

        selected_month = col2.selectbox("Selecione o Mês", 
                                        options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                        format_func=lambda x: pd.to_datetime(f'2024-{x:02d}-01').strftime('%B'),
                                        index=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12].index(last_month))

        # Filter the DataFrame based on the selected year and month
        df_filtered = df[(df['Ano'] == selected_year) & (df['Mês'] == selected_month)]
    
    return df_filtered
