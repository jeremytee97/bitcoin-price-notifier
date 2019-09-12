import requests
import time
from facebook_login_details import receiver_id, sender_email, sender_password
from datetime import datetime
from facebook_messenger import send_message
from fbchat import Client

# change this before using it
BITCOIN_PRICE_THRESHOLD = 10010
BITCOIN_NOTIFICATION_NUMBER = 5


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


def main():
    bitcoin_history = []
    client = Client(sender_email, sender_password)
    while True:
        price = get_bitcoin_price()
        current_datetime = datetime.now()
        bitcoin_history.append({'datetime': current_datetime, 'price': price})

        # Send an emergency notification when below threshold
        if price < BITCOIN_PRICE_THRESHOLD:
            send_message(client, receiver_id, price, code=EMERGENCY_CODE)

        # Send an update notification
        if len(bitcoin_history) == BITCOIN_NOTIFICATION_NUMBER:  # Once we have 5 items in our bitcoin_history send an update
            send_message(client, receiver_id, bitcoin_history)
            # Reset the history
            bitcoin_history = []

        # Sleep for 5 minutes (for testing purposes you can set it to a lower number)
        time.sleep(5 * 60)


if __name__ == '__main__':
    main()