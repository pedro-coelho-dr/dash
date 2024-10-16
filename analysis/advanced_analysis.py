import streamlit as st
import pandas as pd
import plotly.express as px
from database.db_handler import get_Transactions_Dataframe, TransactionTypeEnum
from analysis.utils import filter_df_date


# Função para gerar gráfico de barras sobrepostas dos saldos por categoria
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



# Função para gerar gráfico sunburst das porcentagens de receitas e despesas por categoria com melhorias de visualização
def plot_sunburst_chart(df):
    df_copy = df.copy()

    # Converter as strings de categorias em listas
    df_copy['Categorias'] = df_copy['Categorias'].str.split(', ')

    # "Explodir" a coluna de categorias para ter uma linha por categoria
    df_exploded = df_copy.explode('Categorias')

    # Agrupar por categoria e tipo (Receita/Despesa) para obter o total por tipo dentro de cada categoria
    sunburst_data = df_exploded.groupby(['Categorias', 'Tipo'])['Valor'].sum().reset_index()

    # Calcular o valor total para cada tipo (Receita/Despesa) e o valor por categoria para calcular as porcentagens
    total_values = sunburst_data.groupby('Tipo')['Valor'].sum().reset_index()
    sunburst_data = sunburst_data.merge(total_values, on='Tipo', suffixes=('', '_Total'))

    # Calcular a porcentagem de cada categoria dentro de seu tipo (Receita ou Despesa)
    sunburst_data['Porcentagem'] = (sunburst_data['Valor'] / sunburst_data['Valor_Total']) * 100

    # Criar gráfico sunburst
    st.subheader("📊 Gráfico Sunburst: Porcentagens de Receita e Despesa por Categoria")
    fig = px.sunburst(sunburst_data, 
                      path=['Tipo', 'Categorias'], 
                      values='Porcentagem', 
                      color='Tipo', 
                      color_discrete_map={"Receita": "#09AB3B", "Despesa": "#FF2B2B"}, 
                      title='Porcentagem de Receita e Despesa por Categoria',
                      labels={'Porcentagem': 'Porcentagem (%)', 'Categorias': 'Categorias'},
                      hover_data={'Valor': True})

    # Ajustar o layout para aumentar o tamanho do gráfico e melhorar a visualização
    fig.update_layout(
        width=900,  # Largura do gráfico
        height=700,  # Altura do gráfico
        margin=dict(t=50, l=25, r=25, b=25),  # Ajuste das margens
        sunburstcolorway=["#09AB3B", "#FF2B2B"],  # Paleta de cores personalizada
    )

    # Melhorar as divisões
    fig.update_traces(
        marker=dict(
            line=dict(color="white", width=2)  # Aumentar a espessura das divisões
        )
    )

    st.plotly_chart(fig)

    # Dropdown para selecionar a categoria e exibir informações detalhadas
    st.subheader("🔍 Detalhes da Categoria Selecionada")
    
    # Criar uma lista de opções para o dropdown
    categorias_unicas = sunburst_data['Categorias'].unique().tolist()
    
    # Adicionar a opção de selecionar todas
    categorias_unicas.insert(0, 'Todas as Categorias')

    # Dropdown para selecionar uma categoria
    categoria_selecionada = st.selectbox("Selecione uma Categoria para ver detalhes", categorias_unicas)
    
    # Filtrar os dados com base na categoria selecionada
    if categoria_selecionada == 'Todas as Categorias':
        detalhes_categoria = sunburst_data  # Mostrar todos os dados
    else:
        detalhes_categoria = sunburst_data[sunburst_data['Categorias'] == categoria_selecionada]

    # Exibir os detalhes da categoria selecionada
    st.write(detalhes_categoria[['Tipo', 'Categorias', 'Valor', 'Porcentagem']])


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
    df['Data'] = pd.to_datetime(df['Data'])  # Certificar que 'Data' está no formato datetime
    df = df.sort_values(by="Data", ascending=False)  # Ordena pela coluna 'Data'
    df = filter_df_date(df)


    if not df.empty:
        # Exibir diferentes gráficos
        plot_overlapped_bar_chart(df)
        plot_sunburst_chart(df)
        plot_line_chart(df)
        plot_area_chart(df)
        plot_scatter_chart(df)
    else:
        st.write("Nenhuma transação disponível.")

# Executar a análise avançada
if __name__ == '__main__':
    advanced_analysis()
