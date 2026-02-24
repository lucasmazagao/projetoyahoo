import pandas as pd
from xgboost import XGBRegressor, XGBClassifier
from tickers import tickers_atuais
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def treinamento(df_ticker, ticker):
    df = df_ticker.dropna().copy()

    eliminar_cols = ['Date', 'Ticker', 'Setor', 'Industria', 'Target']
    feature_cols = [c for c in df.columns if c not in eliminar_cols]

    x = df[feature_cols]
    y = df['Target']

    if len(df) < 10:
        print(f'[{ticker}] dados insuficientes')
        return None

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, shuffle=False)

    # modelo
    modelo = XGBClassifier(
        n_estimators=100,
        max_depth=3,
        learning_rate=0.1
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

    for ticker in tickers:
        try:
            df_ticker = df.loc[df['Ticker'] == ticker].copy()
            df_res = treinamento(df_ticker, ticker)

            if df_res is not None:
                resultados.append(df_res)

        except Exception as e:
            print(f"Erro no ticker {ticker}: {e}")

    if resultados:
        df_previsoes = pd.concat(resultados, ignore_index=True)
        df_previsoes.to_csv('previsoes_mk1.csv', index=False)