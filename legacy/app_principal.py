import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 1. CONFIGURAÇÃO DA PÁGINA E TEMA ESCURO (CSS)
st.set_page_config(page_title="Quant IA Brasil - Alpha v2.0", layout="wide", page_icon="🌐")

st.markdown("""
    <style>
    /* Forçando fundo escuro e estilo terminal */
    .stApp {
        background-color: #0b0e14;
        color: #a3a8b8;
    }
    h1, h2, h3 { color: #ffffff !important; font-family: 'Courier New', monospace; }
    /* Estilo dos cartões de métricas */
    div[data-testid="metric-container"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 15px;
        border-radius: 8px;
    }
    div[data-testid="metric-container"] > div > div > div {
        color: #00ffa3 !important; /* Verde neon para valores */
    }
    .titulo-secao {
        color: #8b949e; font-size: 14px; font-weight: bold; letter-spacing: 2px;
        margin-bottom: 10px; margin-top: 20px; text-transform: uppercase;
    }
    </style>
""", unsafe_allow_html=True)

# 2. FUNÇÕES PARA BUSCAR DADOS REAIS
@st.cache_data(ttl=900) # Atualiza a cada 15 min
def buscar_dados_mercado():
    tickers = {"IBOV": "^BVSP", "USD/BRL": "BRL=X", "BTC": "BTC-USD"}
    dados = {}
    for nome, ticker in tickers.items():
        try:
            hist = yf.Ticker(ticker).history(period="2d")
            hoje = hist['Close'].iloc[-1]
            ontem = hist['Close'].iloc[-2]
            var_pct = ((hoje - ontem) / ontem) * 100
            dados[nome] = {"valor": hoje, "var": var_pct}
        except (KeyError, IndexError) as e:
            print(f"[AVISO] sem dados para {ticker}: {str(e)}")
            dados[nome] = {"valor": 0, "var": 0}
        except Exception as e:
            print(f"[ERRO] falha ao buscar {ticker}: {str(e)}")
            dados[nome] = {"valor": 0, "var": 0}
    return dados

@st.cache_data(ttl=3600)
def buscar_historico_grafico():
    # Pega últimos 3 meses do IBOV e de uma carteira simulada (ex: PETR4) para comparar
    ibov = yf.Ticker("^BVSP").history(period="3mo")['Close']
    estrategia = yf.Ticker("PETR4.SA").history(period="3mo")['Close'] * 100 # Escala para bater com ibov
    
    df = pd.DataFrame({'Mercado (IBOV)': ibov, 'Estratégia Quant': estrategia}).dropna()
    # Normaliza base 100 para comparar performance
    df = (df / df.iloc[0]) * 100 
    return df

dados_macro = buscar_dados_mercado()
grafico_df = buscar_historico_grafico()

# ==========================================
# 3. CONSTRUÇÃO DA INTERFACE (LAYOUT)
# ==========================================

# HEADER
st.markdown("<h1>🌐 QUANT IA BRASIL <span style='color:#00ffa3; font-size: 20px;'>ALPHA V2.0</span> <span style='float:right; font-size:16px; color:#8b949e;'>🟢 AO VIVO</span></h1>", unsafe_allow_html=True)
st.markdown("---")

# DIVISÃO PRINCIPAL: 70% ESQUERDA (Gráficos) | 30% DIREITA (Notícias e Alertas)
col_esq, col_dir = st.columns([7, 3])

with col_esq:
    # LINHA 1: SCORE DE MERCADO E MÉTRICAS MACRO
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("IBOV / BOVA11", f"{dados_macro['IBOV']['valor']:,.0f}", f"{dados_macro['IBOV']['var']:.2f}%")
    c2.metric("BITCOIN BTC", f"$ {dados_macro['BTC']['valor']:,.0f}", f"{dados_macro['BTC']['var']:.2f}%")
    c3.metric("SELIC / CDI", "10.75%", "0.00%") # Fixo para o exemplo
    c4.metric("USD / BRL", f"R$ {dados_macro['USD/BRL']['valor']:.2f}", f"{dados_macro['USD/BRL']['var']:.2f}%")

    st.markdown("<div class='titulo-secao'>PERFORMANCE COMPARATIVA</div>", unsafe_allow_html=True)
    
    # GRÁFICO PRINCIPAL (PLOTLY)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=grafico_df.index, y=grafico_df['Mercado (IBOV)'], name='Mercado (IBOV)', line=dict(color='#2196f3', width=2)))
    fig.add_trace(go.Scatter(x=grafico_df.index, y=grafico_df['Estratégia Quant'], name='Estratégia Alpha', line=dict(color='#00ffa3', width=3)))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#8b949e'),
        margin=dict(l=0, r=0, t=30, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig.update_xaxes(showgrid=True, gridcolor='#30363d')
    fig.update_yaxes(showgrid=True, gridcolor='#30363d')
    st.plotly_chart(fig, use_container_width=True)

with col_dir:
    # LINHA DO TEMPO / NOTÍCIAS (Inspirado na sua imagem)
    st.markdown("<div class='titulo-secao'>🔴 ALERTAS & SINAIS</div>", unsafe_allow_html=True)
    st.info("**🟢 COMPRA: Golden Cross em PETR4**\nMA50 cruzou MA200 para cima. Sinal forte de tendência.")
    st.warning("**⚠️ ATENÇÃO: Volatilidade do BTC**\nMovimento atípico detectado no volume da Binance.")

    st.markdown("<div class='titulo-secao'>📊 INDICADORES MACRO</div>", unsafe_allow_html=True)
    col_m1, col_m2 = st.columns(2)
    col_m1.metric("IPCA (12M)", "4.62%", "acima da meta")
    col_m2.metric("DXY (DÓLAR)", "103.4", "-0.8%")

    st.markdown("<div class='titulo-secao'>📰 NOTÍCIAS & SENTIMENTO</div>", unsafe_allow_html=True)
    
    # Simulação das Notícias com barra de sentimento
    noticias = [
        {"fonte": "INFOMONEY", "titulo": "Ibovespa sobe com dados positivos e alívio no câmbio", "sentimento": 78},
        {"fonte": "VALOR ECONÔMICO", "titulo": "Fed mantém juros e sinaliza corte no semestre", "sentimento": 62},
        {"fonte": "REUTERS BR", "titulo": "Bitcoin supera resistências após ETFs", "sentimento": 88}
    ]

    for noti in noticias:
        st.markdown(f"<span style='color:#00ffa3; font-size:12px;'>{noti['fonte']}</span>", unsafe_allow_html=True)
        st.markdown(f"<span style='color:#ffffff; font-size:14px;'>{noti['titulo']}</span>", unsafe_allow_html=True)
        # Barra de progresso para o sentimento
        st.progress(noti['sentimento'] / 100)
        st.markdown("<br>", unsafe_allow_html=True)