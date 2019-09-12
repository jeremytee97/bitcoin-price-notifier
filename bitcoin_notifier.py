import requests
import time
from facebook_login_details import receiver_id, sender_email, sender_password
from datetime import datetime
from facebook_messenger import send_message
from fbchat import Client


BITCOIN_PRICE_THRESHOLD = 11050
BITCOIN_API_URL = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'
EMERGENCY_CODE = 1


def get_bitcoin_price():
    """
    :return: current bitcoin price in usd (float)
    """
    response = requests.get(BITCOIN_API_URL)
    response_json = response.json()
    # return only the price_usd as that is what we are concern
    return float(response_json[0]['price_usd'])


def format_notification_message(bitcoin_details):
    rows = []
    for detail in bitcoin_details:
        date = detail['datetime'].strftime('%d.%m.%Y %H:%M')  # Formats the date into a string: '24.02.2018 15:09'
        price = detail['price']
        row = '{}: ${}'.format(date, price)
        rows.append(row)

    return '<br>'.join(rows)


def main():
    bitcoin_history = []
    while True:
        price = get_bitcoin_price()
        current_datetime = datetime.now()
        bitcoin_history.append({'datetime': current_datetime, 'price': price})

        # Send an emergency notification when below threshold
        if price < BITCOIN_PRICE_THRESHOLD:
            client = Client(sender_email, sender_password)
            send_message(client, receiver_id, price, code=EMERGENCY_CODE)


if __name__ == '__main__':
    main()