from fbchat.models import *


def send_message(sender, receiver, content, code = 0):
    """
    :param code:  code is to differentiate between emergency notification from update notification
    """

    user_id = receiver
    user = sender.fetchUserInfo(user_id)[user_id]
    print("user's name: {}".format(user.name))

    # format notification if it is emergency notification
    if code:
        message = 'The bitcoin price is now below the threshold at ${}'.format(content)
    else:
        message = format_notification_message(content)

    msg_id = sender.send(Message(text=message), thread_id=user_id, thread_type=ThreadType.USER)

    sender.onMessageDelivered(msg_ids=msg_id,
                              delivered_for=user.name,
                              thread_id=user_id,
                              thread_type=ThreadType.USER,
                              ts=1)

    # client.logout()
    print('Message sent.')
    return


def format_notification_message(bitcoin_details):
    rows = []

    for detail in bitcoin_details:
        date = detail['datetime'].strftime('%d.%m.%Y %H:%M')  # Formats the date into a string: '24.02.2018 15:09'
        price = detail['price']
        row = 'Date {}: ${} '.format(date, price)
        rows.append(row)

    return '\n'.join(rows)

