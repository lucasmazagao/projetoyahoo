import pandas as pd
from xgboost import XGBClassifier
from tickers import tickers_atuais
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from log import log_aviso, log_info

def treinamento(df_ticker, ticker):
    df = df_ticker.dropna().copy()

    eliminar_cols = ['Date', 'Ticker', 'Setor', 'Industria', 'Target']
    feature_cols = [c for c in df.columns if c not in eliminar_cols]

    x = df[feature_cols]
    y = df['Target']

    if len(df) < 50:
        log_aviso(f"treinamento — [{ticker}] dados insuficientes ({len(df)} linhas), ticker ignorado")
        return None

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, shuffle=False)

    # modelo
    modelo = XGBClassifier(
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

    modelo.fit(x_train, y_train)

    # acurácia no conjunto de teste
    predicao_teste = modelo.predict(x_test)
    acuracia = accuracy_score(y_test, predicao_teste)

    # predição do próximo dia útil
    ultima_linha = x.iloc[[-1]]
    ultima_data  = pd.to_datetime(df['Date'].iloc[-1])
    proxima_data = ultima_data + pd.tseries.offsets.BDay(1)

    previsao = modelo.predict(ultima_linha)[0]
    prob = modelo.predict_proba(ultima_linha)[0]

    df_resultado = pd.DataFrame({
        'Date': [proxima_data.strftime('%Y-%m-%d')],
        'Ticker': [ticker],
        'previsao': [int(previsao)],
        'probabilidade': [round(prob[1], 4)],
        'acuracia': [round(acuracia, 4)]
    })

    return df_resultado


def treino_mk1(tickers):
    df = pd.read_csv('mk1.csv')
    resultados = []
    erros = []

    for ticker in tickers:
        try:
            df_ticker = df.loc[df['Ticker'] == ticker].copy()
            df_res = treinamento(df_ticker, ticker)

            if df_res is not None:
                resultados.append(df_res)

        except Exception as e:
            erros.append(ticker)
            log_aviso(f"treino_mk1 — erro no ticker {ticker}: {e}")

    if erros:
        log_aviso(f"treino_mk1 — {len(erros)} ticker(s) com falha: {erros}")

    if resultados:
        df_previsoes = pd.concat(resultados, ignore_index=True)
        df_previsoes.to_csv('previsoes_mk1.csv', index=False)
        log_info(f"treino_mk1 — {len(resultados)} modelos treinados | previsoes_mk1.csv salvo")
    else:
        log_aviso("treino_mk1 — nenhum resultado gerado")


def estrategia(df_previsoes):
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
    
    df_estrategia.to_csv('estrategia_mk1.csv', index=False)