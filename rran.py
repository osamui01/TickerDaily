import requests
import pandas as pd
from openpyxl import load_workbook
from datetime import datetime

API_KEY = '7UE784WXAQFPGQAQ'
TICKER = 'TSCO.LON'
OUTPUT_SIZE = 'compact'
OUTPUT_FILE = 'daily_price.xlsx'

def fetch_price_data(ticker, api_key):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={TICKER}&outputsize={OUTPUT_SIZE}&apikey={API_KEY}'
    res = requests.get(url)
    if res.status_code != 200:
        raise ConnectionError(f"Failed to fetch data: {res.status_code}")
    data = res.json()
    if 'Time Series (Daily)' not in data:
        raise ValueError("No price data found in response. Check API key and ticker symbol.")
    return data

def parse_price_data(data):
    price_time_series = data.get('Time Series (Daily)', {})
    records = []

    for date, metrics in price_time_series.items():
        record = {
            'Date': date,
            'Open': metrics.get('1. open'),
            'High': metrics.get('2. high'),
            'Low': metrics.get('3. low'),
            'Close': metrics.get('4. close'),
            'Volume': metrics.get('5. volume'),
        }
        records.append(record)

    dframe = pd.DataFrame(records)
    dframe['Date'] = pd.to_datetime(dframe['Date'])
    dframe.sort_values('Date', inplace=True)
    return dframe

def populate_excel(dframe, filename):
    try:
        book = load_workbook(filename)
    except FileNotFoundError:
        book = None
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        if book:
            writer.book = book
        dframe.to_excel(writer, index=False, sheet_name=datetime.now().strftime('%Y-%m-%d'))
        writer.save()

def main():
    try:
        data = fetch_price_data(TICKER, API_KEY)
        dframe = parse_price_data(data)
        populate_excel(dframe, OUTPUT_FILE)
        print(f'Data for {TICKER} written to {OUTPUT_FILE}')
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
