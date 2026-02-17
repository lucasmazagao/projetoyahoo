import yfinance as yf
import pandas as pd
from tickers import tickers_atuais

def extrator_acoes(tickers):
    dados_acoes = []
    erro = []

    for ticker in tickers:
        try:
            acao = yf.Ticker(ticker)
            info = acao.info
            dados_acoes.append({
                'Símbolo': ticker,
                'Setor': info.get('sector', ''),
                'Indústria': info.get('industry', ''),
                'Preço Atual': info.get('currentPrice', 0),
                'Preço Máximo 52 Semanas': info.get('fiftyTwoWeekHigh', 0),
                'Preço Mínimo 52 Semanas': info.get('fiftyTwoWeekLow', 0),
                'Volume Médio Diário': info.get('averageDailyVolume10Day', 0),
            })

        except Exception as e:
            erro.append(ticker)
            continue

    df_acoes = pd.DataFrame(dados_acoes)
    df_acoes.to_csv('dados_acoes.csv', index=False)