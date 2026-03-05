import requests
from textblob import TextBlob
from core.database.database import create_connection

NEWS_API_KEY = "6be567e795204d649f123fb0dcd4d3b8"

def analyze_sentiment(text):
    """
    Analisa o sentimento de um texto usando TextBlob.

    Args:
        text (str): Texto a analisar.

    Returns:
        float: Polaridade do sentimento (-1 a 1).
    """
    if not text: return 0.0
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

def collect_news(query="brazil stock market"):
    """
    Coleta notícias via NewsAPI e salva com análise de sentimento.

    Args:
        query (str): Termo de busca para notícias.
    """
    url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    
    try:
        response = requests.get(url, timeout=10)
        articles = response.json().get("articles", [])
    except Exception as e:
        print(f"Erro na NewsAPI: {e}")
        return

    conn = create_connection()
    cursor = conn.cursor()

    for art in articles:
        sentiment_score = analyze_sentiment(art.get("description", ""))
        
        cursor.execute("""
            INSERT OR IGNORE INTO news (title, published_at, source, description, sentiment)
            VALUES (?, ?, ?, ?, ?)
        """, (art["title"], art["publishedAt"], art["source"]["name"], art.get("description", ""), sentiment_score))

    conn.commit()
    conn.close()
    print(f"Eficiência: {len(articles)} notícias analisadas e armazenadas.")