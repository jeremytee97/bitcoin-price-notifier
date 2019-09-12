from fbchat import Client
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
        content = 'The bitcoin price is now below the threshold at ${}'.format(content)

    msg_id = sender.send(Message(text=content), thread_id=user_id, thread_type=ThreadType.USER)

    sender.onMessageDelivered(msg_ids=msg_id,
                              delivered_for=user.name,
                              thread_id=user_id,
                              thread_type=ThreadType.USER,
                              ts=1)

    # client.logout()
    print('Message sent.')
    return



