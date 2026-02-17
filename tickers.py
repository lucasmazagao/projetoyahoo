import requests
from bs4 import BeautifulSoup

def tickers_atuais():
    url = 'https://www.slickcharts.com/sp500'
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    
    tickers = []

    rows = table.find_all('tr')[1:]
    
    for row in rows:
        columns = row.find_all('td')
        if len(columns) >= 3:
            ticker = columns[2].text.strip()
            tickers.append(ticker)
    
    return tickers