import sqlite3

def create_connection():
    """
    Cria conexão com o banco SQLite e inicializa tabelas se necessário.

    Returns:
        sqlite3.Connection: Conexão com o banco.
    """
    conn = sqlite3.connect("market_data.db")
    cursor = conn.cursor()

    # STOCKS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stocks (
        ticker TEXT,
        date TEXT,
        close REAL,
        volume REAL,
        PRIMARY KEY (ticker, date)
    )
    """)

    # GLOBAL MARKETS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS global_markets (
        symbol TEXT,
        date TEXT,
        close REAL,
        volume REAL,
        PRIMARY KEY (symbol, date)
    )
    """)

    # CRYPTO
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS crypto (
        symbol TEXT,
        date TEXT,
        close REAL,
        volume REAL,
        PRIMARY KEY (symbol, date)
    )
    """)

    # NEWS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS news (
        title TEXT,
        published_at TEXT,
        source TEXT,
        description TEXT,
        sentiment REAL,
        PRIMARY KEY (title, published_at)
    )
    """)

    # USUARIOS (Tabela Nova)
    #   - armazenaremos aqui o nome, username e a senha em formato hash (bcrypt);
    #     nunca armazene senhas em texto puro. O aplicativo cuidará do hashing.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # PORTFOLIO (Tabela Nova vinculada ao Usuário)
    # NOTA: coluna 'dividendo_por_cota' é DEPRECATED
    #   - direitos: dividendos agora são buscados dinamicamente via API (Yahoo Finance)
    #   - mantida por compatibilidade com registros antigos
    #   - novos cálculos ignoram esse valor e usam sempre dados da API
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS portfolio (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        ticker TEXT,
        quantidade REAL,
        preco_medio REAL,
        dividendo_por_cota REAL,
        FOREIGN KEY(username) REFERENCES usuarios(username)
    )
    """)

    conn.commit()
    return conn

if __name__ == "__main__":
    # Executar este arquivo diretamente garante que todas as tabelas sejam criadas
    create_connection()
    print("Banco de dados 'market_data.db' inicializado com sucesso.")