from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def train_model(df):
    """
    Treina modelo RandomForest para prever alta de preço em 5 dias.

    Args:
        df (pd.DataFrame): DataFrame com indicadores técnicos.

    Returns:
        tuple: (modelo treinado, acurácia)
    """
    df['future_return'] = df['Close'].pct_change(5).shift(-5)
    df['target'] = (df['future_return'] > 0).astype(int)
    df.dropna(inplace=True)

    features = [
    'rsi',
    'ema50',
    'ema200',
    'macd',
    'volume_ratio',
    'volatility'
]

    X = df[features]
    y = df['target']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)

    return model, accuracy