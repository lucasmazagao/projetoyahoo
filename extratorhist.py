import yfinance as yf
import pandas as pd

def extrator_historico(tickers):
    historico_acoes = []
    erro = []

    for ticker in tickers[:1]:
        try:
            acao = yf.Ticker(ticker)
            historico = acao.history(period='5y')
            historico['Símbolo'] = ticker
            historico_acoes.append(historico)

        except Exception as e:
            erro.append(ticker)
            continue

    df_historico = pd.concat(historico_acoes)
    return df_historico