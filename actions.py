import json
from urllib import request
from datetime import datetime
from con import foxbit, contact


def save_foxbit():
    url = 'https://api.blinktrade.com/api/v1/BRL/ticker?crypto_currency=BTC'
    resp = request.urlopen(url).read()
    data = json.loads(resp.decode('utf-8'))
    data['timestamp'] = datetime.utcnow()
    last_data = foxbit.find().sort('timestamp', -1)
    if last_data.count() > 0:
        last_data = last_data[0]
        if last_data['last'] != data['last']:
            foxbit.insert(data)
            send_notification(data)
    else:
        foxbit.insert(data)
        send_notification(data)


def save_contact(data):
    contact.insert(data)


def send_notification(data):
    """
    TODO Implement notification system.
    """
    pass
