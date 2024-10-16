from datetime import timedelta
import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit_lightweight_charts.dataSamples as data
from database.db_handler import get_Transactions_Dataframe

# Filtrar periodo de analise
def filter_df_date(df):
    st.subheader("📅 Filtrar por Período")
    # Checkbox para ativar filtro customizado
    if st.checkbox("Usar filtro personalizado de período"):
        # Seção de filtro por período
        col1, col2 = st.columns(2)
        start_date = col1.date_input("Data de Início", df['Data'].max().date() - timedelta(days=30))
        end_date = col2.date_input("Data de Fim", df['Data'].max().date())

        # Filtrar o DataFrame pelas datas selecionadas
        df = df[(df['Data'] >= pd.to_datetime(start_date)) & 
                                    (df['Data'] <= pd.to_datetime(end_date))]
    else:

        # Adicionar colunas de ano e mês para facilitar o filtro
        df['Ano'] = df['Data'].dt.year
        df['Mês'] = df['Data'].dt.month

        # Filtro por ano e mês
        col1, col2 = st.columns(2)
        # Obter o último ano e mês a partir dos dados
        last_year = df['Ano'].max()
        last_month = df[df['Ano'] == last_year]['Mês'].max()

        # Seleção do ano com o último ano como padrão
        selected_year = col1.selectbox("Selecione o Ano", 
                                    options=sorted(df['Ano'].unique(), reverse=True),
                                    index=sorted(df['Ano'].unique(), reverse=True).index(last_year))

        # Seleção do mês com o último mês como padrão
        selected_month = col2.selectbox("Selecione o Mês", 
                                        options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                        format_func=lambda x: pd.to_datetime(f'2024-{x:02d}-01').strftime('%B'),
                                        index=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12].index(last_month))

        # Filtrar o DataFrame com base no mês e ano selecionados
        df = df[(df['Ano'] == selected_year) & (df['Mês'] == selected_month)]
        
    return df





def balance_histogram():
    df = get_Transactions_Dataframe()
    print(df.head())
    print(data.priceVolumeSeriesHistogram)




# testar analises
if __name__ == '__main__':
    balance_histogram()