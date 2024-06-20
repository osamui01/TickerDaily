import requests
import pandas as pd
from openpyxl import load_workbook
from datetime import datetime


# Keys = 'CC080TMHE8UX4NMX', '7UE784WXAQFPGQAQ'
API_KEY = '7UE784WXAQFPGQAQ'
TICKER = 'TSCO.LON'
OUTPUT_FILE = ''

def fetch_price_data(TICKER, API_KEY):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={TICKER}&outputsize=compact&apikey={API_KEY}'
    res = requests.get(url)
    data = res.json()
    return data

def parse_price_data(data):
    price_time_series = data.get('Time Series (Daily)', {})
    if not price_time_series:
        raise ValueError("No price data found.")
    
    records = []

    for date, metrics in price_time_series.items():
        record ={
            'Date': date,
            'Open': metrics['1. open'],
            'High': metrics['2. high'],
            'Low': metrics['3. low'],
            'Close': metrics['4. close'],
            'Volume': metrics['5. volume'],
        }
        records.append(record)

    dframe = pd.DataFrame(records)
    dframe['Date'] = pd.to_datetime(dframe['Date'])
    dframe.sort_values('Date', inplace=True)
    print(dframe)
    return dframe

def populate_excel(dframe, filename):
    try:
        book = load_workbook(filename)
        writer = pd.ExcelWriter(filename, engine='openpyxl')
        writer.book = book;
    except FileNotFoundError:
        writer = pd.ExcelWriter(filename, engine='openpyxl')

    dframe.to_excel(writer, index=False, sheet_name=datetime.now().strftime('%Y-%m-%d'))
    writer.save()
    writer.close()

def main():
    data = fetch_price_data(TICKER, API_KEY)
    dframe = parse_price_data(data)
    populate_excel(dframe, OUTPUT_FILE)
    print(f'Data for {TICKER} written to {OUTPUT_FILE}')

if __name__ == '__main__':
    main()


# Notes for Demo
# 
# The script can be set to run daily using Windows Task Scheduler
# This allows for price updates at the start/end of different sessions
#  
# Record instance of running the script
# Record instance of excel file population
# 
# 