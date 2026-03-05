from data.market_data import get_stock_data
from indicators.technical import add_indicators
from models.ml_model import train_model
from engines.regime_engine import detect_regime
from engines.ai_assistant import get_ai_recommendation

def run_conversational_analysis(ticker):
    # 1. Dados e Indicadores
    df = get_stock_data(ticker)
    df = add_indicators(df)

    # 2. Inteligência Quantitativa
    model, accuracy, features = train_model(df)
    last_data = df[features].iloc[-1:]
    prob = model.predict_proba(last_data)[0][1]

    # 3. Contexto Macro
    regime = detect_regime()

    # 4. Geração da Recomendação Estilo "Assistente"
    report = get_ai_recommendation(ticker, prob, accuracy, regime)
    
    print(report)

if __name__ == "__main__":
    # Agora podes rodar para qualquer ativo e ele te responde como um assistente
    ticker = input("Qual ativo deseja analisar? (ex: PETR4.SA, BTC-USD): ")
    run_conversational_analysis(ticker)