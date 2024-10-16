from datetime import timedelta
import streamlit as st
import pandas as pd
import plotly.express as px

from streamlit_lightweight_charts import renderLightweightCharts
import streamlit_lightweight_charts.dataSamples as data


from database.db_handler import get_Transactions_Dataframe


# Função para calcular o saldo diário
def calculate_daily_balance(df):
    # Agrupar por data e calcular o saldo
    df_grouped = df.groupby(df['Data'].dt.date).agg(
        Saldo=('Valor', lambda x: x[df['Tipo'] == 'Receita'].sum() - x[df['Tipo'] == 'Despesa'].sum())
    ).reset_index()
    df_grouped['Data'] = pd.to_datetime(df_grouped['Data'])  # Certificando-se de que a coluna Data está no formato correto
    return df_grouped

# Função para transformar o DataFrame em uma lista de dicionários
def df_to_histogram_data(df):
    histogram_data = []
    
    # Calcular o saldo diário
    df = calculate_daily_balance(df)
    
    # Definir a cor do saldo em relação ao dia anterior
    for i in range(len(df)):
        color = 'rgba(0, 150, 136, 0.8)' if i == 0 or df['Saldo'].iloc[i] >= df['Saldo'].iloc[i - 1] else 'rgba(255,82,82, 0.8)'
        
        data_dict = {
            'time': df['Data'].iloc[i].strftime('%Y-%m-%d'),  # Data no formato YYYY-MM-DD
            'value': df['Saldo'].iloc[i],  # Saldo do dia
            'color': color
        }
        histogram_data.append(data_dict)
    
    return histogram_data

def balance_histogram(df):

    # Converter o DataFrame
    histogram_data = df_to_histogram_data(df)

    # Configurações do gráfico
    priceVolumeChartOptions = {
        "height": 400,
        "rightPriceScale": {
            "scaleMargins": {
                "top": 0.2,
                "bottom": 0.25,
            },
            "borderVisible": False,
        },
        "overlayPriceScales": {
            "scaleMargins": {
                "top": 0.7,
                "bottom": 0,
            }
        },
        "layout": {
            "background": {
                "type": 'solid',
                "color": '#131722'
            },
            "textColor": '#d1d4dc',
        },
        "grid": {
            "vertLines": {
                "color": 'rgba(42, 46, 57, 0)',
            },
            "horzLines": {
                "color": 'rgba(42, 46, 57, 0.6)',
            }
        }
    }

    # Dados de exemplo para a série do gráfico
    priceVolumeSeries = [
        {
            "type": 'Area',
            "data": histogram_data,
            "options": {
                "topColor": 'rgba(38,198,218, 0.56)',
                "bottomColor": 'rgba(38,198,218, 0.04)',
                "lineColor": 'rgba(38,198,218, 1)',
                "lineWidth": 2,
            }
        },
        {
            "type": 'Histogram',
            "data": histogram_data,
            "options": {
                "color": '#26a69a',
                "priceFormat": {
                    "type": 'volume',
                },
                "priceScaleId": "volume",
            },
            "priceScale": {
                "scaleMargins": {
                    "top": 0.7,
                    "bottom": 0,
                }
            }
        }
    ]

    # Exibir gráfico no Streamlit
    renderLightweightCharts([
        {
            "chart": priceVolumeChartOptions,
            "series": priceVolumeSeries
        }
    ], 'priceAndVolume')

# testar analises
if __name__ == '__main__':
    df = get_Transactions_Dataframe()  # Chame a função para obter o DataFrame de transações
    balance_histogram(df)
