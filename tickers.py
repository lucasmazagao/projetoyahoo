import requests
from bs4 import BeautifulSoup
from log import log_aviso, log_info

def tickers_atuais():
    url = 'https://www.slickcharts.com/sp500'
    headers = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')

    if table is None:
        log_aviso("tickers_atuais — tabela S&P 500 não encontrada na página")
        return []

    tickers = []
    rows = table.find_all('tr')[1:]

    for row in rows:
        columns = row.find_all('td')
        if len(columns) >= 3:
            ticker = columns[2].text.strip()
            tickers.append(ticker)

    log_info(f"tickers_atuais — {len(tickers)} tickers obtidos")
    return tickers