import requests
import time
from datetime import datetime

BITCOIN_PRICE_THRESHOLD = 10050
BITCOIN_API_URL = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'

def get_bitcoin_price():
    response = requests.get(BITCOIN_API_URL)
    response_json = response.json()
    #return only the price_usd as that is what we are concern
    return float(response_json[0]['price_usd'])

