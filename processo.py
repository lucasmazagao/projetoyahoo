import pandas as pd

def process_serie():
    # vai limpar dados, gerar df_ohlcv
    df_ohlcv = pd.read_csv('dados_historico.csv')
    df_ohlcv = df_ohlcv[['Date', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Volume']]
    
    df_ohlcv['Date'] = pd.to_datetime(df_ohlcv['Date'], utc=True)
    df_ohlcv = df_ohlcv.sort_values(['Ticker', 'Date']).reset_index(drop=True)
    df_ohlcv['Date'] = df_ohlcv['Date'].dt.date
    
    df_ohlcv.to_csv('ohlcv5y.csv', index=False)

'''
def process_fund():
    df_fund = pd.read_csv('dados_fund.csv')

    df_fund.to_csv('fund.csv', index=False)'''
