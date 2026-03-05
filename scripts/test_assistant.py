import pandas as pd
import sqlite3
import sys
import os

# --- REFORÇO DE CAMINHO ---
# Garante que a raiz do projeto seja vista para importar core.*
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.append(root_path)

from core.engines.ai_assistant import get_ai_recommendation
from core.data.market_data import get_stock_data
from core.indicators.technical import add_indicators
from core.models.ml_model import train_model
from core.engines.regime_engine import detect_regime

def testar_assistente(ticker="PETR4.SA"):
    """
    Testa o assistente IA com um ticker de exemplo.

    Args:
        ticker (str): Símbolo do ativo a testar.
    """
    print(f"🔍 Iniciando teste de diagnóstico para: {ticker}...")

    try:
        # 1. Simulação de Coleta e Indicadores
        df = get_stock_data(ticker)
        df = add_indicators(df)
        
        # 2. Treino rápido do Modelo
        features = ['rsi', 'ema50', 'ema200', 'macd', 'volume_ratio', 'volatility']
        model, accuracy = train_model(df)
        last_data = df[features].iloc[-1:]
        prob = model.predict_proba(last_data)[0][1]

        # 3. Detecção de Regime de Mercado
        # Nota: Certifica-te que rodaste o global_collector pelo menos uma vez
        try:
            regime = detect_regime()
        except:
            regime = "Indeterminado (Faltam dados globais)"

        # 4. Geração do Relatório Conversacional
        print("\n" + "="*40)
        print("🤖 RESPOSTA DO ASSISTENTE EM TESTE")
        print("="*40)
        
        relatorio = get_ai_recommendation(ticker, prob, accuracy, regime)
        print(relatorio)

    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        print("Dica: Verifique se o banco market_data.db existe e tem dados.")

if __name__ == "__main__":
    testar_assistente()