import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split

def treinamento(df_ticker, ticker):
    df = df_ticker.dropna().copy()

    eliminar_cols = ['Date', 'Ticker', 'Setor', 'Industria', 'Target']
    feature_cols = [c for c in df.columns if c not in eliminar_cols]

    x = df[feature_cols]
    y = df['Target']

    if len(df) < 100:
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
        'probabilidade': [round(prob[1], 4)]
    })

    return df_resultado


def treino_mk1(tickers, inicio):
    df = pd.read_csv('mk1.csv')
    df = df[df['Date'] <= inicio].copy()

    resultados = []

    for ticker in tickers:
        try:
            df_ticker = df.loc[df['Ticker'] == ticker].copy()
            df_res = treinamento(df_ticker, ticker)

            if df_res is not None:
                resultados.append(df_res)

        except:
            pass

    if resultados:
        df_previsoes = pd.concat(resultados, ignore_index=True)
        return df_previsoes

def estrategia(df_previsoes):
    ultimo_dia = df_previsoes['Date'].max()
    df_ultimo  = df_previsoes[df_previsoes['Date'] == ultimo_dia]

    buy_flags  = []
    sell_flags = []

    for _, row in df_ultimo.iterrows():
        if row['previsao'] == 1 and row['probabilidade'] >= 0.7:
            buy_flags.append(row['Ticker'])
        elif row['previsao'] == 0 and row['probabilidade'] >= 0.7:
            sell_flags.append(row['Ticker'])

    df_estrategia = pd.DataFrame({
        'Ticker': df_ultimo['Ticker'].values,
        'Flag': [
            '1'  if t in buy_flags  else
            '-1' if t in sell_flags else
            '0'
            for t in df_ultimo['Ticker'].values
        ]
    })

    return df_estrategia

def efetivar_estrategia(backtest_resultados, df_estrategia, capital, posicoes, inicio):
    """
    Executa as ordens do dia `inicio` e registra o resultado no histórico.

    Parâmetros
    ----------
    backtest_resultados : pd.DataFrame  — histórico acumulado dos dias anteriores
    df_estrategia       : pd.DataFrame  — flags do dia (colunas: Ticker, Flag)
    capital             : float         — caixa disponível antes das ordens do dia
    posicoes            : dict          — estado da carteira:
                                          { ticker: {'qtd': float, 'preco_entrada': float} }
    inicio              : pd.Timestamp  — data do dia sendo processado

    Retorna
    -------
    (backtest_resultados, capital, posicoes) atualizados
    """
    ALOCACAO = 0.10  # 10% do capital disponível por compra

    # preços de fechamento do dia para todos os tickers com sinal
    df_mk1 = pd.read_csv('mk1.csv')
    df_mk1['Date'] = pd.to_datetime(df_mk1['Date'])
    precos_dia = (
        df_mk1[df_mk1['Date'] == inicio]
        .set_index('Ticker')['Close']
        .to_dict()
    )

    # --- executa as ordens ---
    for _, row in df_estrategia.iterrows():
        ticker = row['Ticker']
        flag   = int(row['Flag'])
        preco  = precos_dia.get(ticker)

        if preco is None or preco <= 0:
            continue

        if flag == 1 and ticker not in posicoes:
            # compra: abre posição com 10% do capital disponível
            valor_aloc = capital * ALOCACAO
            if valor_aloc > 0:
                qtd = valor_aloc / preco
                posicoes[ticker] = {'qtd': qtd, 'preco_entrada': preco}
                capital -= valor_aloc

        elif flag == -1 and ticker in posicoes:
            # venda: fecha posição e devolve ao caixa
            pos     = posicoes.pop(ticker)
            receita = pos['qtd'] * preco
            capital += receita

    # --- mark-to-market: reavalia posições abertas com o Close do dia ---
    valor_carteira = sum(
        pos['qtd'] * precos_dia.get(tk, pos['preco_entrada'])
        for tk, pos in posicoes.items()
    )

    total = capital + valor_carteira

    # variação percentual em relação ao dia anterior
    if not backtest_resultados.empty:
        total_anterior = backtest_resultados['Total'].iloc[-1]
        shift = round((total - total_anterior) / total_anterior * 100, 4) if total_anterior else 0.0
    else:
        shift = 0.0

    nova_linha = pd.DataFrame([{
        'Date':     inicio,
        'Capital':  round(capital, 2),
        'Carteira': round(valor_carteira, 2),
        'Total':    round(total, 2),
        'Shift':    shift,
    }])

    backtest_resultados = pd.concat([backtest_resultados, nova_linha], ignore_index=True)

    return backtest_resultados, capital, posicoes


def backtest(tickers):
    # primeiro eliminar 100 ultimos dias
    # conta com 100000 de capital inicial
    # para cada dia, para cada ticker, se estrategia indicar compra, comprar com 10% do capital disponivel
    # a cada dia, calcular o valor da carteira (capital + valor das posicoes) e guardar em um historico
    # no proximo dia, realizar vendas, registrar compras, atualizar o valor da carteira, e assim por diante
    # registrar valor para cada posicao comprada, para calcular o valor da carteira a cada dia
    # no final do periodo de backtest, calcular o retorno total

    hoje   = pd.Timestamp('today').normalize()
    inicio = hoje - pd.tseries.offsets.BDay(100)

    capital  = 100_000.0
    posicoes = {}   # { ticker: {'qtd': float, 'preco_entrada': float} }

    backtest_resultados = pd.DataFrame(columns=['Date', 'Capital', 'Carteira', 'Total', 'Shift'])

    while inicio <= hoje:
        df_previsoes = treino_mk1(tickers, inicio)

        if df_previsoes is None or df_previsoes.empty:
            inicio += pd.tseries.offsets.BDay(1)
            continue

        df_estrategia = estrategia(df_previsoes)

        backtest_resultados, capital, posicoes = efetivar_estrategia(
            backtest_resultados, df_estrategia, capital, posicoes, inicio
        )

        inicio += pd.tseries.offsets.BDay(1)

    retorno_total = round((backtest_resultados['Total'].iloc[-1] / 100_000.0 - 1) * 100, 2)
    print(f"Retorno total no período: {retorno_total}%")

    return backtest_resultados
