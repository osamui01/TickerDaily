import requests
import pandas as pd
from datetime import datetime

# Keys = 'CC080TMHE8UX4NMX', '7UE784WXAQFPGQAQ'
API_KEY = '7UE784WXAQFPGQAQ'
ticker = 'TSCO.LON'

def fetch_price_data(ticker, API_KEY):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize=compact&apikey={API_KEY}'
    res = requests.get(url)
    try:
        res.raise_for_status()  # Raise an HTTPError for bad responses
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        print('Response content:', res.text)
        raise

    data = res.json()
    return data

def parse_price_data(data):
    if 'Note' in data:
        print("API limit reached or another issue:", data['Note'])
        raise ValueError("API limit reached or another issue.")
    
    if 'Time Series (Daily)' not in data:
        print("Debug: Full API response:", data)
        raise ValueError("No price data found.")
    
    price_time_series = data['Time Series (Daily)']
    
    records = []
    for date, metrics in price_time_series.items():
        try:
            record = {
                'Date': date,
                'Open': float(metrics['1. open']),
                'High': float(metrics['2. high']),
                'Low': float(metrics['3. low']),
                'Close': float(metrics['4. close']),
                'Volume': int(metrics['5. volume']),
            }
            records.append(record)
        except KeyError as key_err:
            print(f"Key error: {key_err}")
            print(f"Data for date {date}: {metrics}")
            raise
        except ValueError as val_err:
            print(f"Value conversion error: {val_err}")
            print(f"Data for date {date}: {metrics}")
            raise

    dframe = pd.DataFrame(records)
    dframe['Date'] = pd.to_datetime(dframe['Date'])
    dframe.sort_values('Date', inplace=True)
    print(dframe)
    return dframe

try:
    data = fetch_price_data(ticker, API_KEY)
    parse_price_data(data)
except requests.exceptions.HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
except ValueError as val_err:
    print(f'Value error: {val_err}')
except Exception as err:
    print(f'Other error occurred: {err}')
