from datetime import timedelta
import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit_lightweight_charts.dataSamples as data
from database.db_handler import get_Transactions_Dataframe


def balance_histogram():
    df = get_Transactions_Dataframe()
    print(df.head())
    print(data.priceVolumeSeriesHistogram)




# testar analises
if __name__ == '__main__':
    balance_histogram()