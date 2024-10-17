import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts

# Exemplo de dados simulados para receitas e despesas
receitas_data = [
    {"time": "2024-10-01", "value": 500},
    {"time": "2024-10-02", "value": 700},
    {"time": "2024-10-03", "value": 600},
    {"time": "2024-10-04", "value": 900},
]

despesas_data = [
    {"time": "2024-10-01", "value": 300},
    {"time": "2024-10-02", "value": 200},
    {"time": "2024-10-03", "value": 400},
    {"time": "2024-10-04", "value": 500},
]


def format_df_for_chart(df, tipo: str):
    """
    Formata o DataFrame para o gráfico, agrupando por data e somando os valores
    para cada tipo de transação (Receita ou Despesa).
    """
    # Filtrar o DataFrame pelo tipo de transação (Receita ou Despesa)
    tipo_df = df[df['Tipo'] == tipo][['Data', 'Valor']]
    
    # Agrupar por data e somar os valores
    tipo_df = tipo_df.groupby('Data').sum().reset_index()
    
    # Converter as datas para o formato 'YYYY-MM-DD' e preparar a lista de dicionários
    tipo_data = tipo_df.apply(lambda row: {"time": row['Data'].strftime('%Y-%m-%d'), "value": row['Valor']}, axis=1).tolist()
    
    return tipo_data


def income_outcome_area(df):

    receitas_data = format_df_for_chart(df, "Receita")
    despesas_data = format_df_for_chart(df, "Despesa")




   # Configurações gerais do gráfico
    overlaidAreaSeriesOptions = {
        "height": 400,
        "rightPriceScale": {
            "scaleMargins": {
                "top": 0.1,
                "bottom": 0.1,
            },
            "mode": 0,  # PriceScaleMode: 0-Normal, 1-Logarithmic, 2-Percentage, 3-IndexedTo100
            "borderColor": 'rgba(197, 203, 206, 0.4)',
        },
        "timeScale": {
            "borderColor": 'rgba(197, 203, 206, 0.4)',
        },
        "layout": {
            "background": {
                "type": 'solid',
                "color": '#131722'
            },
            "textColor": '#ffffff',
        },
        "grid": {
            "vertLines": {
                "color": 'rgba(197, 203, 206, 0.4)',
                "style": 1,  # LineStyle: 0-Solid, 1-Dotted, 2-Dashed, 3-LargeDashed
            },
            "horzLines": {
                "color": 'rgba(197, 203, 206, 0.4)',
                "style": 1,  # LineStyle: 0-Solid, 1-Dotted, 2-Dashed, 3-LargeDashed
            }
        }
    }

    # Séries de dados para receitas (verde) e despesas (vermelho)
    seriesOverlaidChart = [
        {
            "type": 'Area',
            "data": receitas_data,
            "options": {
                "topColor": 'rgba(0, 255, 100, 0.7)',  # Verde
                "bottomColor": 'rgba(0, 255, 0, 0.3)',
                "lineColor": 'rgba(0, 255, 0, 1)',
                "lineWidth": 2,
            },
        },
        {
            "type": 'Area',
            "data": despesas_data,
            "options": {
                "topColor": 'rgba(255, 0, 0, 0.7)',  # Vermelho
                "bottomColor": 'rgba(255, 0, 100, 0.3)',
                "lineColor": 'rgba(255, 0, 0, 1)',
                "lineWidth": 2,
            },
        }
    ]

    # Renderizando o gráfico
    st.subheader("Gráfico de Receitas (Verde) vs Despesas (Vermelho)")

    renderLightweightCharts([
        {
            "chart": overlaidAreaSeriesOptions,
            "series": seriesOverlaidChart
        }
    ], 'overlaid_chart')
