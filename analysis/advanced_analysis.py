import streamlit as st
import pandas as pd
import plotly.express as px
from database.db_handler import get_Transactions_Dataframe, TransactionTypeEnum
from utils.filter_df_date import filter_df_date


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
    st.subheader("📊 Porcentagens de Receita e Despesa por Categoria")
    fig = px.sunburst(sunburst_data, 
                      path=['Tipo', 'Categorias'], 
                      values='Porcentagem', 
                      color='Tipo', 
                      color_discrete_map={"Receita": "#09AB3B", "Despesa": "#FF2B2B"}, 
                      title='Porcentagem de Receita e Despesa por Categoria',
                      labels={'Porcentagem': 'Porcentagem (%)', 'Categorias': 'Categorias'},
                      hover_data={'Valor': True})

    fig.update_layout(
        width=900,
        height=700,
        margin=dict(t=50, l=25, r=25, b=25),
        sunburstcolorway=["#09AB3B", "#FF2B2B"],
    )

    fig.update_traces(
        marker=dict(
            line=dict(color="white", width=2)
        )
    )

    st.plotly_chart(fig)

    # Separar receitas e despesas
    df_receitas = sunburst_data[sunburst_data['Tipo'] == 'Receita'].sort_values(by=['Valor'], ascending=False)
    df_despesas = sunburst_data[sunburst_data['Tipo'] == 'Despesa'].sort_values(by=['Valor'], ascending=False)

    col1, col2 = st.columns(2)

    # Tabela de Receitas
    with col1:
        st.markdown("### 💰 Detalhes de Receitas")
        if not df_receitas.empty:
            st.table(df_receitas[['Categorias', 'Valor', 'Porcentagem']].style.format({
                'Valor': 'R$ {:,.2f}', 'Porcentagem': '{:.2f}%'
            }))
        else:
            st.write("Nenhuma receita disponível.")

    # Tabela de Despesas
    with col2:
        st.markdown("### 💸 Detalhes de Despesas")
        if not df_despesas.empty:
            st.table(df_despesas[['Categorias', 'Valor', 'Porcentagem']].style.format({
                'Valor': 'R$ {:,.2f}', 'Porcentagem': '{:.2f}%'
            }))
        else:
            st.write("Nenhuma despesa disponível.")


# Função para gerar gráfico de barras sobrepostas dos saldos por categoria
def plot_overlapped_bar_chart(df):
    df_copy = df.copy()
    df_copy['Categorias'] = df_copy['Categorias'].str.split(', ')
    df_exploded = df_copy.explode('Categorias')

    bar_data = df_exploded.groupby(['Categorias', 'Tipo'])['Valor'].sum().reset_index()

    st.subheader("📊 Receita e Despesa por Categoria")
    fig = px.bar(bar_data, x='Categorias', y='Valor', color='Tipo', barmode='group',
                 labels={'Valor': 'Valor (R$)', 'Categorias': 'Categorias'},
                 title='Receita e Despesa por Categoria (Comparação lado a lado)',
                 color_discrete_map={"Receita": "#09AB3B", "Despesa": "#FF2B2B"})
    
    st.plotly_chart(fig)



# Função para gerar gráficos de dispersão separados por despesa e receita, com cores diferentes
def plot_scatter_chart(df):
    df_copy = df.copy()

    # Separar as categorias por vírgulas e "explodir" em múltiplas linhas
    df_copy['Categorias'] = df_copy['Categorias'].str.split(', ')  # Separar as categorias em listas
    df_exploded = df_copy.explode('Categorias')  # Explodir para múltiplas linhas por categoria

    # Gráfico de Dispersão para Despesas
    st.subheader("🔍 Valor por Categoria (Despesas)")
    df_despesas = df_exploded[df_exploded['Tipo'] == 'Despesa']  # Filtrar apenas despesas
    fig_despesas = px.scatter(df_despesas, x='Categorias', y='Valor', size='Valor',
                              title='Valor da Despesa por Categoria',
                              labels={'Categorias': 'Categorias', 'Valor': 'Valor (R$)'},
                              color_discrete_sequence=['#FF2B2B'])  # Vermelho para despesas
    fig_despesas.update_layout(
        width=900,
        height=500,
        showlegend=False  # Remover legenda
    )
    st.plotly_chart(fig_despesas)

    # Gráfico de Dispersão para Receitas
    st.subheader("🔍 Valor por Categoria (Receitas)")
    df_receitas = df_exploded[df_exploded['Tipo'] == 'Receita']  # Filtrar apenas receitas
    fig_receitas = px.scatter(df_receitas, x='Categorias', y='Valor', size='Valor',
                              title='Valor da Receita por Categoria',
                              labels={'Categorias': 'Categorias', 'Valor': 'Valor (R$)'},
                              color_discrete_sequence=['#09AB3B'])  # Verde para receitas
    fig_receitas.update_layout(
        width=900,
        height=500,
        showlegend=False  # Remover legenda
    )
    st.plotly_chart(fig_receitas)





# Seção de Análise Avançada
def advanced_analysis():
    st.title("Análise Avançada")

    df = get_Transactions_Dataframe()
    df['Data'] = pd.to_datetime(df['Data'])
    df = df.sort_values(by="Data", ascending=False)
    df = filter_df_date(df)

    if not df.empty:
        
        plot_overlapped_bar_chart(df)
        plot_scatter_chart(df)
        plot_sunburst_chart(df)
    else:
        st.write("Nenhuma transação disponível.")


if __name__ == '__main__':
    advanced_analysis()
