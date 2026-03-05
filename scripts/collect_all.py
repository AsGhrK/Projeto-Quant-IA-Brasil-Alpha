import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.data.stocks_collector import collect_stock_data
from core.data.news_collector import collect_news
from core.data.global_collector import collect_global_data
from core.data.crypto_collector import collect_crypto_data

def run_collection():
    # Coletar ações brasileiras populares
    stocks_br = ["PETR4.SA", "VALE3.SA", "ITUB4.SA", "ABEV3.SA", "BBAS3.SA", "BBDC4.SA", "MGLU3.SA", "WEGE3.SA", "ITSA4.SA", "JBSS3.SA"]
    for stock in stocks_br:
        collect_stock_data(stock)

    collect_global_data()
    collect_crypto_data()

    collect_news("brazil stock market")
    collect_news("crypto market")
    collect_news("global economy")

    print("Coleta expandida concluída!")

if __name__ == "__main__":
    run_collection()