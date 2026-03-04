import yfinance as yf
import pandas as pd
from log import log_aviso, log_info

def extrator_historico(tickers):
    historico_acoes = []
    erros = []

    for ticker in tickers:
        try:
            acao = yf.Ticker(ticker)
            historico = acao.history(period='5y', interval='1d')
            historico['Ticker'] = ticker
            historico_acoes.append(historico)

        except Exception as e:
            erros.append(ticker)
            log_aviso(f"extrator_historico — falha em {ticker}: {e}")
            continue

    if erros:
        log_aviso(f"extrator_historico — {len(erros)} ticker(s) com erro: {erros}")

    log_info(f"extrator_historico — {len(historico_acoes)} séries históricas obtidas")

    df_historico = pd.concat(historico_acoes)
    df_historico.to_csv('dados_historico.csv', index=True)