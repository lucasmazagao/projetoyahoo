import yfinance as yf
import pandas as pd

def extrator_acoes(tickers):
    dados_acoes = []
    erro = []

    for ticker in tickers:
        try:
            acao = yf.Ticker(ticker)
            info = acao.info
            
            dados_acoes.append({
                # basicos
                'Ticker': ticker,
                'Setor': info.get('sector', ''),
                'Indústria': info.get('industry', ''),
                
                # precos
                'Preço Atual': info.get('currentPrice', 0),
                'Preço Máximo 52 Semanas': info.get('fiftyTwoWeekHigh', 0),
                'Preço Mínimo 52 Semanas': info.get('fiftyTwoWeekLow', 0),
                
                # mkt cap
                'Volume Médio Diário': info.get('averageDailyVolume10Day', 0),
                'Market Cap': info.get('marketCap', 0),
                
                # avaliacoes de mercado
                'P/L': info.get('trailingPE', None),
                'P/L Futuro': info.get('forwardPE', None),
                'P/VP': info.get('priceToBook', None),
                'PEG Ratio': info.get('pegRatio', None),
                
                # rent
                'Margem Lucro': info.get('profitMargins', None),
                'ROE': info.get('returnOnEquity', None),
                'ROA': info.get('returnOnAssets', None),
                'Crescimento Receita': info.get('revenueGrowth', None),
                
                # yield
                'Dividend Yield': info.get('dividendYield', None),
                
                # risco
                'Beta': info.get('beta', None),
                'Dívida/Patrimônio': info.get('debtToEquity', None),
                'Short Ratio': info.get('shortRatio', None),
            })

        except Exception as e:
            erro.append(ticker)
            continue

    df_acoes = pd.DataFrame(dados_acoes)
    df_acoes.to_csv('fund.csv', index=False)