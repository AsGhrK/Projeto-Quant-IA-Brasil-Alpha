import yfinance as yf
import pandas as pd
import streamlit as st

@st.cache_data(ttl=900)
def get_stock_data(ticker, period="1y"):
    """
    Busca dados históricos de preços e volume via yfinance.

    Args:
        ticker (str): Símbolo do ativo.
        period (str): Período histórico (ex: '1y').

    Returns:
        pd.DataFrame: DataFrame com Close e Volume.
    """
    data = yf.download(ticker, period=period, interval="1d")

    # Corrige possível MultiIndex
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data = data[['Close', 'Volume']]
    data['Close'] = data['Close'].squeeze()

    data.dropna(inplace=True)

    return data