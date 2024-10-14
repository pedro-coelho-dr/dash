import streamlit as st
import pandas as pd
import plotly.express as px
from database.db_handler import get_Transactions_Dataframe, TransactionTypeEnum


# Função para gerar gráfico de barras sobrepostas
def plot_overlapped_bar_chart(df):
    df_copy = df.copy()

    # Converter as strings de categorias em listas
    df_copy['Categorias'] = df_copy['Categorias'].str.split(', ')

    # "Explodir" a coluna de categorias para ter uma linha por categoria
    df_exploded = df_copy.explode('Categorias')

    # Agrupar por categoria e tipo (Receita/Despesa) para obter o total por tipo dentro de cada categoria
    bar_data = df_exploded.groupby(['Categorias', 'Tipo'])['Valor'].sum().reset_index()

    # Criar gráfico de barras sobrepostas
    st.subheader("📊 Gráfico de Barras Sobrepostas: Receita e Despesa por Categoria")
    fig = px.bar(bar_data, x='Categorias', y='Valor', color='Tipo', barmode='group',
                 labels={'Valor': 'Valor (R$)', 'Categorias': 'Categorias'},
                 title='Receita e Despesa por Categoria (Comparação lado a lado)',
                 color_discrete_map={"Receita": "#09AB3B", "Despesa": "#FF2B2B"})  # Especificar as cores
    
    st.plotly_chart(fig)


# Função para gerar gráfico de linhas
def plot_line_chart(df):
    df_copy = df.copy()
    st.subheader("📈 Gráfico de Linhas: Valor ao Longo do Tempo")
    st.line_chart(df_copy.set_index('Data')['Valor'])  # Usar Data e Valor

# Função para gerar gráfico de área
def plot_area_chart(df):
    df_copy = df.copy()

    st.subheader("📊 Gráfico de Área: Valor Acumulado ao Longo do Tempo")
    df_copy['Valor Acumulado'] = df_copy['Valor'].cumsum()  # Calcular valor acumulado
    st.area_chart(df_copy.set_index('Data')['Valor Acumulado'])  # Usar Data e Valor Acumulado

# Função para gerar gráfico de dispersão
def plot_scatter_chart(df):
    df_copy = df.copy()
    st.subheader("🔍 Gráfico de Dispersão: Valor por Categoria")
    fig = px.scatter(df_copy, x='Categorias', y='Valor', color='Tipo', size='Valor',
                     title='Valor da Transação por Categoria')
    st.plotly_chart(fig)

# Seção de Análise Avançada
def advanced_analysis():
    st.title("📊 Análise Avançada - Comparação de Categorias")

    # Carregar transações do banco de dados
    df = get_Transactions_Dataframe()

    if not df.empty:
        # Exibir diferentes gráficos
        plot_overlapped_bar_chart(df)
        plot_line_chart(df)
        plot_area_chart(df)
        plot_scatter_chart(df)
    else:
        st.write("Nenhuma transação disponível.")

# Executar a análise avançada
if __name__ == '__main__':
    advanced_analysis()
