import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def query_prices(ticker, date):
    payload = {'function': 'TIME_SERIES_DAILY', 'symbol': ticker, 'outputsize': 'full', 'apikey': os.getenv("ALPHA_VANTAGE_API_KEY")}
    r = requests.get('https://www.alphavantage.co/query', params=payload)

    time_series = r.json()["Time Series (Daily)"]


    return time_series[date]["4. close"]
