import pandas as pd
# features modelo 1

def create_features_xgboost():
    df_ohlcv = pd.read_csv("ohlcv5y.csv")
    df_fund = pd.read_csv("fund.csv")

    # para xgboost pegamos tudo disponivel
    df = pd.merge(df_ohlcv, df_fund, on="ticker", how="left")

    # Create target variable
    df["Sinal"] = (df["close"].shift(-1) > df["close"]).astype(int)

    # Feature engineering
    df["return"] = df["close"].pct_change()
    df["volatility"] = df["return"].rolling(window=21).std()
    df["momentum"] = df["close"].diff(21)

    return df

# features modelo 2

def create_features_2():
    pass
