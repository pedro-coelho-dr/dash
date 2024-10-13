import streamlit as st
import pandas as pd
import plotly.express as px
from database.db_handler import get_all_transactions, TransactionTypeEnum

# Função para carregar transações e convertê-las em um DataFrame do pandas
def load_transactions():
    transactions = get_all_transactions()

    # Converter transações em um DataFrame
    data = {
        'date': [t.date for t in transactions],
        'type': ["Receita" if t.type == TransactionTypeEnum.CREDITO else "Despesa" for t in transactions],
        'value': [t.value for t in transactions],
        'categories': [", ".join([cat.name for cat in t.categories]) for t in transactions],
        'description': [t.description for t in transactions],
    }

    return pd.DataFrame(data)

# Função para gerar gráfico de barras
def plot_bar_chart(df):
    st.subheader("📊 Gráfico de Barras: Total por Categoria")
    bar_data = df.groupby('categories')['value'].sum().sort_values(ascending=False)
    st.bar_chart(bar_data)

# Função para gerar gráfico de linhas
def plot_line_chart(df):
    st.subheader("📈 Gráfico de Linhas: Valor ao Longo do Tempo")
    df_sorted = df.sort_values(by='date')
    st.line_chart(df_sorted.set_index('date')['value'])

# Função para gerar gráfico de área
def plot_area_chart(df):
    st.subheader("📊 Gráfico de Área: Valor Acumulado ao Longo do Tempo")
    df_sorted = df.sort_values(by='date')
    df_sorted['cumulative_value'] = df_sorted['value'].cumsum()
    st.area_chart(df_sorted.set_index('date')['cumulative_value'])

# Função para gerar gráfico de dispersão
def plot_scatter_chart(df):
    st.subheader("🔍 Gráfico de Dispersão: Valor por Categoria")
    fig = px.scatter(df, x='categories', y='value', color='type', size='value',
                     title='Valor da Transação por Categoria')
    st.plotly_chart(fig)

# Seção de Análise Avançada
def advanced_analysis():
    st.title("📊 Análise Avançada - Comparação de Categorias")

    # Carregar transações do banco de dados
    df = load_transactions()

    if not df.empty:
        # Exibir diferentes gráficos
        plot_bar_chart(df)
        plot_line_chart(df)
        plot_area_chart(df)
        plot_scatter_chart(df)
    else:
        st.write("Nenhuma transação disponível.")

# Executar a análise avançada
if __name__ == '__main__':
    advanced_analysis()
