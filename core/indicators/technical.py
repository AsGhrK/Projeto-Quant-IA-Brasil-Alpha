import ta

def add_indicators(df):
    """
    Adiciona indicadores técnicos ao DataFrame.

    Args:
        df (pd.DataFrame): DataFrame com Close e Volume.

    Returns:
        pd.DataFrame: DataFrame com indicadores adicionados.
    """
    df['rsi'] = ta.momentum.RSIIndicator(df['Close']).rsi()
    df['ema50'] = ta.trend.EMAIndicator(df['Close'], window=50).ema_indicator()
    df['ema200'] = ta.trend.EMAIndicator(df['Close'], window=200).ema_indicator()
    df['macd'] = ta.trend.MACD(df['Close']).macd()

    # Volume
    df['volume_mean'] = df['Volume'].rolling(20).mean()
    df['volume_ratio'] = df['Volume'] / df['volume_mean']

    # Volatilidade
    df['volatility'] = df['Close'].pct_change().rolling(20).std()

    df.dropna(inplace=True)

    return df