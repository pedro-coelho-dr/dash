import pandas as pd
from database.db_handler import get_Transactions_Dataframe
from utils.balance_histogram import balance_histogram
from utils.filter_df_date import filter_df_date

dados_exemplo = [
    {'Data': '2024-01-01', 'Valor': 2500, 'Tipo': 'Receita'},
    {'Data': '2024-01-02', 'Valor': 1500, 'Tipo': 'Despesa'},
    {'Data': '2024-01-03', 'Valor': 3200, 'Tipo': 'Receita'},
    {'Data': '2024-01-04', 'Valor': 500, 'Tipo': 'Despesa'},
    {'Data': '2024-01-05', 'Valor': 4200, 'Tipo': 'Receita'},
    {'Data': '2024-01-06', 'Valor': 250, 'Tipo': 'Despesa'},
    {'Data': '2024-01-07', 'Valor': 2800, 'Tipo': 'Receita'},
    {'Data': '2024-01-08', 'Valor': 800, 'Tipo': 'Despesa'},
    {'Data': '2024-01-09', 'Valor': 3400, 'Tipo': 'Receita'},
    {'Data': '2024-01-10', 'Valor': 1200, 'Tipo': 'Despesa'},
    {'Data': '2024-01-11', 'Valor': 2700, 'Tipo': 'Receita'},
    {'Data': '2024-01-12', 'Valor': 1800, 'Tipo': 'Despesa'},
]

df = get_Transactions_Dataframe()
# df = pd.DataFrame(dados_exemplo)

# filtrar dataframe por data
df = filter_df_date(df)
balance_histogram(df)