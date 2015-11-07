# -*- coding: utf-8 -*-
import os
import json
import smtplib
import pytz

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from itertools import chain
from urllib import request

from con import foxbit, contact


def save_foxbit():
    url = 'https://api.blinktrade.com/api/v1/BRL/ticker?crypto_currency=BTC'
    resp = request.urlopen(url).read()
    data = json.loads(resp.decode('utf-8'))
    data['timestamp'] = datetime.now(pytz.timezone('America/Sao_Paulo'))
    last_data = foxbit.find().sort('timestamp', -1)
    if last_data.count() > 0:
        last_data = last_data[0]
        if last_data['last'] != data['last']:
            foxbit.insert_one(data)
        send_notification(data)
    else:
        foxbit.insert_one(data)
        send_notification(data)


def save_contact(data):
    contact.insert_one(data)


def send_notification(data):
    lower_than = contact.find({
        'rules': 'menor',
        'sent': False,
        'value': {'$gt': data['last']}
    })
    upper_than = contact.find({
        'rules': 'maior',
        'sent': False,
        'value': {'$lt': data['last']}
    })

    if lower_than and upper_than:
        all_contacts = [i for i in chain(lower_than, upper_than)]
    elif lower_than and not upper_than:
        all_contacts = lower_than
    elif not lower_than and upper_than:
        all_contacts = upper_than

    username = os.environ.get('MANDRILL_USERNAME', None)
    password = os.environ.get('MANDRILL_PASSWORD', None)
    if username and password:
        smtp = smtplib.SMTP('smtp.mandrillapp.com', 587)
        smtp.login(username, password)
    else:
        smtp = None

    for item in all_contacts:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Bitcoins Notification'
        msg['From'] = 'Bitcoins Notification <contato@bitcoinsnotification.com>'
        msg['To'] = item['email']

        if contact['rules'] == 'menor':
            above_below = 'abaixo'
        else:
            above_below = 'acima'

        text = 'Atenção! O valor do Bitcion está {above_below} de R$ {value}, o Bitcoin está valendo R$ {last}.'
        text = text.format(
            above_below=above_below, value=item['value'], last=data['last'])
        part = MIMEText(text, 'plain')
        if smtp:
            msg.attach(part)
            smtp.sendmail(msg['From'], msg['To'], msg.as_string())
        else:
            # Is running local
            print(text)
            print(msg['From'])
            print(msg['To'])
        contact.update_one({'_id': item['_id']}, {'$set': {'sent': True}})
    if smtp:
        smtp.quit()
