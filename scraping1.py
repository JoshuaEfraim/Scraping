import requests
from bs4 import BeautifulSoup
import csv

url = 'https://finance.yahoo.com/markets/stocks/gainers/'  

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    tickers = soup.select('span.symbol.yf-ravs5v')
    prices = soup.select('fin-streamer[data-field="regularMarketPrice"]')
    changes = soup.select('fin-streamer[data-field="regularMarketChange"]')
    change_percents = soup.select('fin-streamer[data-field="regularMarketChangePercent"]')
    volumes = soup.select('fin-streamer[data-field="regularMarketVolume"]')

    with open('yahoo_finance_stocks.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Ticker', 'Price USD', 'Change', 'Change (%)', 'Volume'])

        for i in range(len(tickers)):
            ticker = tickers[i].text.strip() if i < len(tickers) else 'N/A'
            price = prices[i].text.strip() if i < len(prices) else 'N/A'
            change = changes[i].text.strip() if i < len(changes) else 'N/A'
            change_percent = change_percents[i].text.strip() if i < len(change_percents) else 'N/A'
            volume = volumes[i].text.strip() if i < len(volumes) else 'N/A'

            writer.writerow([ticker, price, change, change_percent, volume])

    print("Stock data has been successfully scraped and saved to 'yahoo_finance_stocks.csv'")

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
