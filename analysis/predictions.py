import streamlit as st
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt
from database.db_handler import get_Transactions_Dataframe
import pandas as pd

# Função para criar série temporal mensal
def criar_saldo_mensal(df):
    df['Saldo'] = df['Valor'].where(df['Tipo'] == 'Receita', -df['Valor'])
    df['Mês'] = df['Data'].dt.to_period('M').apply(lambda r: r.start_time)
    saldo_mensal = df.groupby('Mês')['Saldo'].sum()
    return saldo_mensal

def render_predictions_page():
    st.title("Previsão de Saldo Mensal")

    # Carregar as transações do banco de dados
    df_transactions = get_Transactions_Dataframe()

    if df_transactions.empty:
        st.warning("⚠️ Nenhuma transação encontrada no banco de dados.")
        return

    # Criar a série temporal mensal
    saldo_mensal = criar_saldo_mensal(df_transactions)

    if saldo_mensal.empty or len(saldo_mensal) < 24:
        st.error("⚠️ Dados insuficientes para realizar previsões usando SARIMA.")
        return

    # Determinar o ano corrente
    current_year = pd.Timestamp.now().year
    train_end_year = current_year - 1

    # Dividir os dados em treino e previsão
    train_data = saldo_mensal[:f'{train_end_year}-12-31']

    # Ajustar o modelo SARIMA
    p, d, q = 1, 1, 1
    P, D, Q, m = 1, 1, 1, 12

    try:
        model = SARIMAX(train_data, 
                        order=(p, d, q), 
                        seasonal_order=(P, D, Q, m), 
                        enforce_stationarity=False, 
                        enforce_invertibility=False)
        model_fit = model.fit(disp=False)
    except Exception as e:
        st.error(f"Erro ao ajustar o modelo SARIMA: {e}")
        return

    # Fazer previsões para o ano corrente
    try:
        forecast_steps = 12  # Previsões para os 12 meses do ano corrente
        forecast_start = f'{current_year}-01-01'
        final_predictions = model_fit.get_forecast(steps=forecast_steps)
        forecast_index = pd.date_range(start=forecast_start, periods=forecast_steps, freq='M')
        forecast_values = final_predictions.predicted_mean
    except Exception as e:
        st.error(f"Erro ao fazer previsões para {current_year}: {e}")
        return

    # Plotar as previsões e os dados reais
    try:
        plt.figure(figsize=(12, 6))

        # Plotar os saldos reais mensais do ano corrente
        actual_data = saldo_mensal[f'{current_year}-01-01':f'{current_year}-12-31']
        if not actual_data.empty:
            shifted_actual_data = actual_data.copy()
            shifted_actual_data.index = shifted_actual_data.index.shift(1, freq='M')
            plt.plot(
                shifted_actual_data.index,
                shifted_actual_data.values,
                label="Saldos Reais",
                color="#007BFF",  # Azul vibrante
                marker='o',
                linewidth=2,
                alpha=0.8
            )

        # Plotar as previsões
        plt.plot(
            forecast_index,
            forecast_values,
            label=f"Previsões ({current_year})",
            color="#FFC107",  # Amarelo vibrante
            linestyle="--",
            marker='s',
            linewidth=2,
            alpha=0.9
        )

        # Estilização do gráfico
        plt.title(f"Previsões de Saldo Mensal para {current_year}", fontsize=16, color="#333")
        plt.xlabel("Meses", fontsize=12, color="#555")
        plt.ylabel("Saldo", fontsize=12, color="#555")
        plt.xticks(forecast_index, [date.strftime('%b') for date in forecast_index], rotation=45, fontsize=10)
        plt.legend(fontsize=12, frameon=True, shadow=True, loc="upper left")
        plt.grid(color="#DDDDDD", linestyle="--", linewidth=0.7, alpha=0.7)

        # Adicionar borda ao gráfico
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['left'].set_color('#CCCCCC')
        plt.gca().spines['bottom'].set_color('#CCCCCC')

        st.pyplot(plt)

    except Exception as e:
        st.error(f"Erro ao plotar os resultados: {e}")
