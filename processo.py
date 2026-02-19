import pandas as pd

def processamento():
    df_ohlcv = pd.read_csv('dados_historico.csv')
    df_ohlcv = df_ohlcv[['Date', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Volume']]
    df_ohlcv = df_ohlcv.sort_values(['Ticker', 'Date']).reset_index(drop=True)
    
    df_ohlcv['Date'] = pd.to_datetime(df_ohlcv['Date']).dt.date
    df_ohlcv.to_csv('ohlcv5y.csv', index=False)
