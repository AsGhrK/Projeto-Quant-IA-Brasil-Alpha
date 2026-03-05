import time
import pandas as pd
from data.stocks_collector import collect_stock_data
from data.news_collector import collect_news
from engines.ai_assistant import get_ai_recommendation
from main import run_analysis # Importa sua lógica de ML já existente

# Lista de ativos para o Scanner varrer
WATCHLIST = ["PETR4.SA", "VALE3.SA", "ITUB4.SA", "BTC-USD", "ETH-USD", "SOL-USD"]

def run_elite_scanner():
    print("🌐 [1/3] Atualizando Notícias e Sentimento Global...")
    collect_news("stock market news")
    collect_news("crypto world")

    oportunidades = []

    print(f"📊 [2/3] Escaneando {len(WATCHLIST)} ativos com Machine Learning...")
    for ticker in WATCHLIST:
        try:
            # Coleta dados novos para garantir o tempo real
            collect_stock_data(ticker)
            
            # Aqui rodamos sua lógica do main.py adaptada para retornar os dados
            # (Assumindo que adaptamos o main.py para retornar valores em vez de apenas dar print)
            report, prob = run_analysis_for_scanner(ticker)
            
            if prob > 0.65: # Filtro de Elite: Só o que tem mais de 65% de chance
                oportunidades.append(report)
                
        except Exception as e:
            print(f"⚠️ Erro ao escanear {ticker}: {e}")

    print("\n" + "="*50)
    print("🤖 RELATÓRIO FINAL DO ASSISTENTE - MELHORES OPORTUNIDADES")
    print("="*50)
    
    if not oportunidades:
        print("Aguardando melhores sinais. O mercado está em modo cautela.")
    else:
        for op in oportunidades:
            print(op)

def run_analysis_for_scanner(ticker):
    """
    Versão modificada da sua função main.py para retornar os dados para o scanner.
    """
    from data.market_data import get_stock_data
    from indicators.technical import add_indicators
    from models.ml_model import train_model
    from engines.regime_engine import detect_regime
    from engines.ai_assistant import get_ai_recommendation

    df = get_stock_data(ticker)
    df = add_indicators(df)
    model, accuracy, features = train_model(df)
    last_data = df[features].iloc[-1:]
    prob = model.predict_proba(last_data)[0][1]
    regime = detect_regime()

    # Chama nosso novo assistente conversacional
    report = get_ai_recommendation(ticker, prob, accuracy, regime)
    return report, prob

if __name__ == "__main__":
    run_elite_scanner()