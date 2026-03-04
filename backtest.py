import pandas as pd
from xgboost import XGBClassifier

# ── parâmetros walk-forward ──────────────────────────────────
JANELA_TREINO_DIAS = 252   # ~1 ano mínimo para treinar
JANELA_RETREINO_DIAS = 63  # retreina a cada ~1 trimestre
# ─────────────────────────────────────────────────────────────

hoje = pd.to_datetime('today').date()
data_corte = hoje - pd.tseries.offsets.BDay(100)


def _modelo_xgb():
    return XGBClassifier(
        n_estimators=300,
        max_depth=3,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.7,
        min_child_weight=10,
        reg_alpha=0.05,
        reg_lambda=1.0,
        eval_metric='logloss',
        random_state=42
    )


def treino_bkt(df_ticker, ticker):
    eliminar_cols = ['Date', 'Ticker', 'Setor', 'Industria', 'Target']
    feature_cols  = [c for c in df_ticker.columns if c not in eliminar_cols]

    df = df_ticker.dropna().reset_index(drop=True)

    if len(df) < JANELA_TREINO_DIAS + JANELA_RETREINO_DIAS:
        return None

    resultados = []
    inicio = JANELA_TREINO_DIAS

    while inicio < len(df):
        fim = min(inicio + JANELA_RETREINO_DIAS, len(df))

        treino = df.iloc[:inicio]
        teste  = df.iloc[inicio:fim]

        modelo = _modelo_xgb()
        modelo.fit(treino[feature_cols], treino['Target'])

        probs    = modelo.predict_proba(teste[feature_cols])[:, 1]
        previsao = modelo.predict(teste[feature_cols])

        bloco = pd.DataFrame({
            'Date':          teste['Date'].values,
            'Ticker':        ticker,
            'Close':         teste['Close'].values,
            'previsao':      previsao,
            'probabilidade': probs.round(4),
        })
        resultados.append(bloco)

        inicio = fim

    return pd.concat(resultados, ignore_index=True)


def treino_mk1_bkt(tickers):
    df = pd.read_csv('mk1.csv')
    df = df[df['Date'] <= str(data_corte)].copy()
    resultados = []

    for ticker in tickers:
        df_ticker = df.loc[df['Ticker'] == ticker].copy()
        df_res = treino_bkt(df_ticker, ticker)

        if df_res is not None:
            resultados.append(df_res)

    if not resultados:
        return None

    df_sinais = pd.concat(resultados, ignore_index=True)
    return df_sinais

def estrategia_bkt(df_previsoes):
    buy_flags = []
    sell_flags = []

    for ticker in df_previsoes['Ticker'].unique():
        if df_previsoes[df_previsoes['Ticker'] == ticker].iloc[-1]['previsao'] == 1 and df_previsoes[df_previsoes['Ticker'] == ticker].iloc[-1]['probabilidade'] >= 0.7:
            buy_flags.append(ticker)
        elif df_previsoes[df_previsoes['Ticker'] == ticker].iloc[-1]['previsao'] == 0 and df_previsoes[df_previsoes['Ticker'] == ticker].iloc[-1]['probabilidade'] >= 0.7:
            sell_flags.append(ticker)
    
    df_estrategia = pd.DataFrame({
        'Ticker': df_previsoes['Ticker'].unique(),
        'Flag': ['1' if ticker in buy_flags else '-1' if ticker in sell_flags else '0' for ticker in df_previsoes['Ticker'].unique()]
    })

    return df_estrategia

def backtest(tickers):
    # primeiro eliminar 100 ultimos dias
    # conta com 100000 de capital inicial
    # para cada dia, para cada ticker, se estrategia indicar compra, comprar com 10% do capital disponivel
    # a cada dia, calcular o valor da carteira (capital + valor das posicoes) e guardar em um historico
    # no proximo dia, realizar vendas, registrar compras, atualizar o valor da carteira, e assim por diante
    # registrar valor para cada posicao comprada, para calcular o valor da carteira a cada dia
    # no final do periodo de backtest, calcular o retorno total

    df_previsoes = treino_mk1_bkt(tickers)

    df_estrategia = estrategia_bkt(df_previsoes)

    capital = 100000

    backtest_resultados = pd.DataFrame({
        'Date': [],
        'Capital': [],
        'Carteira': [],
        'Total': [],
        'Shift': []
    })