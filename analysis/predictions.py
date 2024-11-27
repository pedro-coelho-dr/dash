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

# Função para criar série temporal semanal
def criar_saldo_semanal(df):
    df['Saldo'] = df['Valor'].where(df['Tipo'] == 'Receita', -df['Valor'])
    df['Semana'] = df['Data'].dt.to_period('W').apply(lambda r: r.start_time)
    saldo_semanal = df.groupby('Semana')['Saldo'].sum()
    return saldo_semanal

def render_predictions_page():
    st.title("Previsões de Saldo")

    # Carregar as transações do banco de dados
    df_transactions = get_Transactions_Dataframe()

    if df_transactions.empty:
        st.warning("⚠️ Nenhuma transação encontrada no banco de dados.")
        return

    # **Previsão Mensal**
    saldo_mensal = criar_saldo_mensal(df_transactions)
    if len(saldo_mensal) >= 24:
        current_year = pd.Timestamp.now().year
        train_data = saldo_mensal[:f'{current_year - 1}-12-31']

        p, d, q = 1, 1, 1
        P, D, Q, m = 1, 1, 1, 12

        model = SARIMAX(train_data,
                        order=(p, d, q),
                        seasonal_order=(P, D, Q, m),
                        enforce_stationarity=False,
                        enforce_invertibility=False)
        model_fit = model.fit(disp=False)

        forecast_steps = 12
        forecast_index = pd.date_range(start=f'{current_year}-01-01', periods=forecast_steps, freq='M')
        forecast_values = model_fit.get_forecast(steps=forecast_steps).predicted_mean

        # Gerar índices de previsão e deslocar um passo para trás
        forecast_index = pd.date_range(start=f'{current_year}-01-01', periods=forecast_steps, freq='M')
        forecast_index = forecast_index - pd.offsets.MonthBegin(1)  # Deslocar para o início do mês anterior

        # Obter valores previstos
        forecast_values = model_fit.get_forecast(steps=forecast_steps).predicted_mean

        # Gráfico Mensal
        plt.figure(figsize=(12, 6))
        actual_data = saldo_mensal[f'{current_year}-01-01':]
        if not actual_data.empty:
            plt.plot(
                actual_data.index,
                actual_data.values,
                label="Saldos Reais",
                color="#007BFF",
                marker='o',
                linewidth=2
            )

        # Plotar previsões com o índice ajustado
        plt.plot(
            forecast_index,
            forecast_values,
            label="Previsões Mensais",
            color="#FFC107",
            linestyle="--",
            marker='s',
            linewidth=2
        )
        plt.title("Previsões de Saldo Mensal", fontsize=16)
        plt.xlabel("Meses", fontsize=12)
        plt.ylabel("Saldo", fontsize=12)
        plt.xticks(rotation=45)
        plt.legend(fontsize=10)
        plt.grid(alpha=0.4)
        st.pyplot(plt)


    # **Previsão Semanal**
    saldo_semanal = criar_saldo_semanal(df_transactions)
    if len(saldo_semanal) >= 16:
        saldo_semanal_diff = saldo_semanal.diff().dropna()

        total_data = saldo_semanal_diff
        test_data = total_data[-12:]

        p, d, q = 1, 0, 1
        P, D, Q, m = 1, 0, 1, 52

        model = SARIMAX(total_data,
                        order=(p, d, q),
                        seasonal_order=(P, D, Q, m),
                        enforce_stationarity=False,
                        enforce_invertibility=False)
        model_fit = model.fit(disp=False)

        predictions = model_fit.get_prediction(start=test_data.index[0], end=test_data.index[-1]).predicted_mean
        future_predictions = model_fit.forecast(steps=4)
        future_index = pd.date_range(start=test_data.index[-1] + pd.Timedelta(weeks=1), periods=4, freq='W')

        last_known = saldo_semanal.iloc[-len(test_data) - 1]
        predicted_mean_original = last_known + predictions.cumsum()
        future_predictions_original = predicted_mean_original.iloc[-1] + future_predictions.cumsum()

        # **Previsão Semanal**
        saldo_semanal = criar_saldo_semanal(df_transactions)
        if len(saldo_semanal) >= 16:
            saldo_semanal_diff = saldo_semanal.diff().dropna()

            total_data = saldo_semanal_diff
            test_data = total_data[-12:]

            p, d, q = 1, 0, 1
            P, D, Q, m = 1, 0, 1, 52

            model = SARIMAX(total_data,
                            order=(p, d, q),
                            seasonal_order=(P, D, Q, m),
                            enforce_stationarity=False,
                            enforce_invertibility=False)
            model_fit = model.fit(disp=False)

            predictions = model_fit.get_prediction(start=test_data.index[0], end=test_data.index[-1]).predicted_mean
            future_predictions = model_fit.forecast(steps=4)
            future_index = pd.date_range(start=test_data.index[-1] + pd.Timedelta(weeks=1), periods=4, freq='W')

            # Gráfico Semanal
            plt.figure(figsize=(14, 7))
            plt.plot(
                test_data.index,
                test_data,
                label="Dados Reais (Últimas 12 Semanas)",
                color="#007BFF",
                marker="o",
                linewidth=2
            )
            plt.plot(
                predictions.index,
                predictions,
                label="Previsões (Últimas 12 Semanas)",
                color="#FFC107",
                linestyle="--",
                marker="o",
                linewidth=2
            )
            plt.plot(
                future_index,
                future_predictions,
                label="Previsões Futuras (4 Semanas)",
                color="#FFC107",
                linestyle="--",
                marker="o",
                linewidth=2
            )
            plt.title("Previsões Semanais (Últimas 12 Semanas + Próximas 4 Semanas)", fontsize=16)
            plt.xlabel("Semanas", fontsize=12)
            plt.ylabel("Saldo Diferenciado", fontsize=12)
            plt.xticks(rotation=45)
            plt.legend(fontsize=10)
            plt.grid(alpha=0.4)
            st.pyplot(plt)