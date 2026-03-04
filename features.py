import pandas as pd
# features modelo 1

def features_mk1():

    # leitura dos dados e manipulacao inicial
    dfx = pd.read_csv('ohlcv5y.csv')
    df_ohlcv = pd.DataFrame(dfx)

    dfy = pd.read_csv('fund.csv')
    df_fund = pd.DataFrame(dfy)
    df_fund = df_fund[['Ticker', 'Setor', 'Indústria']].rename(columns={'Indústria': 'Industria'})
    
    modelo = df_ohlcv.merge(df_fund, on='Ticker', how='left')

    # funcao de features por ticker
    def tickers(df):
        # medias
        df['sma_20']         = df['Close'].rolling(20).mean()
        df['sma_50']         = df['Close'].rolling(50).mean()
        df['sma_100']        = df['Close'].rolling(100).mean()
        df['price_vs_sma20'] = df['Close'] / df['sma_20'] - 1
        df['price_vs_sma50'] = df['Close'] / df['sma_50'] - 1
        df['sma20_vs_sma50'] = df['sma_20'] / df['sma_50'] - 1

        # retornos
        df['return_1d']  = df['Close'].pct_change(1)
        df['return_5d']  = df['Close'].pct_change(5)
        df['return_20d'] = df['Close'].pct_change(20)
        df['return_60d'] = df['Close'].pct_change(60)

        # volatilidade
        df['volatility_10d'] = df['return_1d'].rolling(10).std()
        df['volatility_20d'] = df['return_1d'].rolling(20).std()

        # volume
        df['volume_sma20'] = df['Volume'].rolling(20).mean()
        df['volume_ratio'] = df['Volume'] / df['volume_sma20']

        return df

    modelo = modelo.groupby('Ticker', group_keys=False).apply(tickers)

    ## features por setor e industria

    # setor_close_avg
    setor = (
        modelo.groupby(['Date', 'Setor'])['Close'].mean()
        .reset_index().rename(columns={'Close': 'setor_close_avg'})
    )

    # setor_close_sma20
    setor_close_aux = (
        modelo.groupby(['Date', 'Setor'])['Close'].mean()
        .reset_index().rename(columns={'Close': 'setor_close_raw'})
    )
    setor_close_aux = setor_close_aux.sort_values(['Setor', 'Date'])
    setor_close_aux['setor_close_sma20'] = (
        setor_close_aux.groupby('Setor')['setor_close_raw']
        .rolling(20).mean().reset_index(level=0, drop=True)
    )
    setor_close_sma20 = setor_close_aux[['Date', 'Setor', 'setor_close_sma20']]

    # setor_vol20
    setor_vol_aux = (
        modelo.groupby(['Date', 'Setor'])['Volume'].mean()
        .reset_index().rename(columns={'Volume': 'setor_vol_raw'})
    )
    setor_vol_aux = setor_vol_aux.sort_values(['Setor', 'Date'])
    setor_vol_aux['setor_vol20'] = (
        setor_vol_aux.groupby('Setor')['setor_vol_raw']
        .rolling(20).std().reset_index(level=0, drop=True)
    )
    setor_vol20 = setor_vol_aux[['Date', 'Setor', 'setor_vol20']]

    # setor_participacao
    setor_volume_total = (
        modelo.groupby(['Date', 'Setor'])['Volume'].sum()
        .reset_index().rename(columns={'Volume': 'setor_volume_total'})
    )
    ticker_volume = (
        modelo.groupby(['Date', 'Ticker', 'Setor'])['Volume'].sum()
        .reset_index().rename(columns={'Volume': 'ticker_volume'})
    )
    setor_participacao = ticker_volume.merge(setor_volume_total, on=['Date', 'Setor'], how='left')
    setor_participacao['setor_participacao'] = (
        setor_participacao['ticker_volume'] / setor_participacao['setor_volume_total']
    )
    setor_participacao = setor_participacao[['Date', 'Ticker', 'Setor', 'setor_participacao']]

    ## features de industria

    # industria_close_avg
    industria = (
        modelo.groupby(['Date', 'Industria'])['Close'].mean()
        .reset_index().rename(columns={'Close': 'industria_close_avg'})
    )

    # industria_close_sma20
    industria_close_aux = (
        modelo.groupby(['Date', 'Industria'])['Close'].mean()
        .reset_index().rename(columns={'Close': 'industria_close_raw'})
    )
    industria_close_aux = industria_close_aux.sort_values(['Industria', 'Date'])
    industria_close_aux['industria_close_sma20'] = (
        industria_close_aux.groupby('Industria')['industria_close_raw']
        .rolling(20).mean().reset_index(level=0, drop=True)
    )
    industria_close_sma20 = industria_close_aux[['Date', 'Industria', 'industria_close_sma20']]

    # industria_vol20
    industria_vol_aux = (
        modelo.groupby(['Date', 'Industria'])['Volume'].mean()
        .reset_index().rename(columns={'Volume': 'industria_vol_raw'})
    )
    industria_vol_aux = industria_vol_aux.sort_values(['Industria', 'Date'])
    industria_vol_aux['industria_vol20'] = (
        industria_vol_aux.groupby('Industria')['industria_vol_raw']
        .rolling(20).std().reset_index(level=0, drop=True)
    )
    industria_vol20 = industria_vol_aux[['Date', 'Industria', 'industria_vol20']]

    # industria_participacao
    industria_volume_total = (
        modelo.groupby(['Date', 'Industria'])['Volume'].sum()
        .reset_index().rename(columns={'Volume': 'industria_volume_total'})
    )
    ticker_volume_ind = (
        modelo.groupby(['Date', 'Ticker', 'Industria'])['Volume'].sum()
        .reset_index().rename(columns={'Volume': 'ticker_volume_ind'})
    )
    industria_participacao = ticker_volume_ind.merge(
        industria_volume_total, on=['Date', 'Industria'], how='left'
    )
    industria_participacao['industria_participacao'] = (
        industria_participacao['ticker_volume_ind'] / industria_participacao['industria_volume_total']
    )
    industria_participacao = industria_participacao[['Date', 'Ticker', 'Industria', 'industria_participacao']]

    # merges intermediarios
    sector_avg = (
        setor.merge(setor_close_sma20, on=['Date', 'Setor'], how='left')
        .merge(setor_vol20, on=['Date', 'Setor'], how='left')
    )
    industry_avg = (
        industria.merge(industria_close_sma20, on=['Date', 'Industria'], how='left')
        .merge(industria_vol20, on=['Date', 'Industria'], how='left')
    )

    # merges finais

    modelo = modelo.merge(sector_avg, on=['Date', 'Setor'], how='left')
    modelo = modelo.merge(industry_avg, on=['Date', 'Industria'], how='left')
    modelo = modelo.merge(setor_participacao, on=['Date', 'Ticker', 'Setor'], how='left')
    modelo = modelo.merge(industria_participacao, on=['Date', 'Ticker', 'Industria'], how='left')

    # target

    def calcular_target(df):
        prox = df['Close'].shift(-1)
        hoje = df['Close']
        df['Target'] = 0
        df.loc[prox > hoje * 1.10, 'Target'] = 1
        df.loc[prox < hoje * 0.95, 'Target'] = -1
        return df

    modelo = modelo.groupby('Ticker', group_keys=False).apply(calcular_target)

    modelo.to_csv('mk1.csv', index=False)

# features modelo 2

def features_mk2():
    pass
