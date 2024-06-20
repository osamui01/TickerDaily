import requests
import pandas as pd
from datetime import datetime
import os

API_KEY = 'FrpspO4LIfKyiXVOq8WxrsvgpCP6H5kT'
TICKER = 'META'
BASE_URL = 'https://api.polygon.io/v2/aggs/ticker/'
OUTPUT_FILE = 'daily_prices.xlsx'

def fetch_price_data(TICKER, API_KEY):
    url = f'{BASE_URL}{TICKER}/range/1/day/2023-01-09/2023-02-10?adjusted=true&sort=asc&apiKey={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        if results:
            result = results[0]
            return {
                'Ticker': TICKER,
                'Open': result['o'],
                'High': result['h'],
                'Low': result['l'],
                'Close': result['c'],
                'Volume': result['v'],
                'Timestamp': datetime.fromtimestamp(result['t'] / 1000) 
            }
    else:
        print(f"Failed to fetch data for {TICKER}: {response.status_code}")
    return None

def populate_spreadsheet(data, file):
    if os.path.exists(file):
        df_existing = pd.read_excel(file)
    else:
        df_existing = pd.DataFrame(columns=['Date', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Volume', 'Timestamp'])

    df_new = pd.DataFrame([data])
    df_new['Date'] = datetime.now().strftime('%Y-%m-%d')

    df_existing.dropna(how='all', inplace=True)

    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    df_combined.to_excel(file, index=False)

def main():
    price_data = fetch_price_data(TICKER, API_KEY)
    if price_data:
        populate_spreadsheet(price_data, OUTPUT_FILE)
        print("Market price updated successfully.")
    else:
        print("No market price was fetched.")

if __name__ == '__main__':
    main()  
