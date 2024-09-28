import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def advanced_analysis():
    st.title("Análise Avançada - Comparação de Categorias")

    # Dados fictícios
    data = {
        'type': ['Receita', 'Receita', 'Despesa', 'Despesa', 'Despesa', 'Receita'],
        'value': [1000, 1500, 700, 400, 300, 2000],
        'category': ['Serviço', 'Venda', 'Materiais', 'Salário', 'Ferramentas', 'Manutenção']
    }

    df = pd.DataFrame(data)

    # Filtrar receitas e despesas
    income = df[df['type'] == 'Receita']
    expenses = df[df['type'] == 'Despesa']

    # Função para exibir o gráfico de comparação de categorias
    def plot_category_comparison():
        # Agrupar por categoria e somar valores
        expense_summary = expenses.groupby('category')['value'].sum()
        income_summary = income.groupby('category')['value'].sum()

        # Criar os gráficos
        fig, ax = plt.subplots(1, 2, figsize=(12, 6))

        # Gráfico de despesas
        ax[0].bar(expense_summary.index, expense_summary.values, color='red')
        ax[0].set_title('Despesas por Categoria')
        ax[0].set_ylabel('Valor (R$)')
        ax[0].set_xlabel('Categoria')

        # Gráfico de receitas
        ax[1].bar(income_summary.index, income_summary.values, color='green')
        ax[1].set_title('Receitas por Categoria')
        ax[1].set_ylabel('Valor (R$)')
        ax[1].set_xlabel('Categoria')

        # Exibir o gráfico no Streamlit
        st.pyplot(fig)

    # Chama a função para exibir o gráfico
    plot_category_comparison()
