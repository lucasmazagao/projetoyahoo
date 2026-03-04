import pandas as pd
from log import log_info, log_aviso

def process_serie():
    df_ohlcv = pd.read_csv('dados_historico.csv')

    df_ohlcv = df_ohlcv[['Date', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Volume']]

    df_ohlcv['Date'] = pd.to_datetime(df_ohlcv['Date'], utc=True)
    df_ohlcv = df_ohlcv.sort_values(['Ticker', 'Date']).reset_index(drop=True)
    df_ohlcv['Date'] = df_ohlcv['Date'].dt.date

    df_ohlcv.to_csv('ohlcv5y.csv', index=False)

    tickers_unicos = df_ohlcv['Ticker'].nunique()
    log_info(f"process_serie — {len(df_ohlcv)} linhas limpas | {tickers_unicos} tickers")
