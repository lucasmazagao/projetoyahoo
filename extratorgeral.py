import yfinance as yf
import pandas as pd
from log import log_aviso, log_info

def extrator_acoes(tickers):
    dados_acoes = []
    erros = []

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
            erros.append(ticker)
            log_aviso(f"extrator_acoes — falha em {ticker}: {e}")
            continue

    if erros:
        log_aviso(f"extrator_acoes — {len(erros)} ticker(s) com erro: {erros}")

    log_info(f"extrator_acoes — {len(dados_acoes)} ações extraídas com sucesso")

    df_acoes = pd.DataFrame(dados_acoes)
    df_acoes.to_csv('fund.csv', index=False)