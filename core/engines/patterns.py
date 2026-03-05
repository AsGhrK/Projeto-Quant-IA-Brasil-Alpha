import pandas as pd

def identify_patterns(df):
    """
    Identifica padrões técnicos no DataFrame.

    Args:
        df (pd.DataFrame): DataFrame com indicadores.

    Returns:
        list: Lista de padrões detectados.
    """
    if df.empty:
        return ["Dados insuficientes para análise de padrões."]
    
    patterns = []
    last_row = df.iloc[-1]
    prev_row = df.iloc[-2]
    
    # 1. Martelo (Hammer) - Padrão de Reversão de Alta
    body = abs(last_row['Close'] - last_row['Open']) if 'Open' in last_row else 0
    # Simplificação para o seu modelo atual:
    if last_row['rsi'] < 30:
        patterns.append("Oversold (Sobrevendido) - RSI abaixo de 30 indica exaustão de venda.")
        
    # 2. Tendência de Médias
    if last_row['ema50'] > last_row['ema200'] and prev_row['ema50'] <= prev_row['ema200']:
        patterns.append("Golden Cross - Cruzamento de alta de longo prazo identificado!")
        
    # 3. Volume Incomum
    if last_row['volume_ratio'] > 2.0:
        patterns.append("Volume Explosivo - Movimento validado por forte entrada de capital.")
        
    return patterns if patterns else ["Nenhum padrão gráfico claro no momento."]