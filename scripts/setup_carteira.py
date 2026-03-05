import sqlite3

def criar_carteira_simulada():
    """
    Cria uma carteira simulada com dados de exemplo para demonstração.
    """
    print("Criando banco de dados da carteira do usuário (Modo Bola de Neve)...")
    conn = sqlite3.connect('market_data.db')
    cursor = conn.cursor()

    # Recria a tabela com a coluna do dividendo por cota
    cursor.execute('DROP TABLE IF EXISTS portfolio')
    cursor.execute('''
    CREATE TABLE portfolio (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker TEXT,
        quantidade REAL,
        preco_medio REAL,
        dividendo_por_cota REAL
    )
    ''')

    # Inserindo dados: Ticker, Cotas que você tem, Preço Médio Pago, Dividendo por Cota (Simulado)
    # Ex: MXRF11 custa perto de R$10 e paga uns R$0,10 por mês.
    ativos_teste = [
        ('PETR4.SA', 30, 32.50, 1.20),   # Paga aprox 1.20 por trimestre
        ('MXRF11.SA', 85, 10.20, 0.10),  # Paga aprox 0.10 por mês
        ('VALE3.SA', 15, 65.00, 2.50)    # Paga aprox 2.50 por semestre
    ]

    cursor.executemany('''
        INSERT INTO portfolio (ticker, quantidade, preco_medio, dividendo_por_cota)
        VALUES (?, ?, ?, ?)
    ''', ativos_teste)

    conn.commit()
    conn.close()
    print("✅ Banco atualizado para o cálculo da Bola de Neve!")

if __name__ == "__main__":
    criar_carteira_simulada()