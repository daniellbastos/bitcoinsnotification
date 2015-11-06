import json
from urllib import request
from datetime import datetime
from con import mongolab, contact


def bitcoinaverage():
    url = 'https://www.mercadobitcoin.net/api/ticker/'
    resp = request.urlopen(url).read()
    data = json.loads(resp.decode('utf-8'))
    data = data['ticker']
    data['timestamp'] = datetime.utcnow()
    last_data = mongolab.find().sort('timestamp', -1)[0]
    if last_data['last'] != data['last']:
        mongolab.insert(data)
        send_notification(data)


def save_contact(data):
    contact.insert(data)


def send_notification(data):
    pass
    """
    if data['last']
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        msg = MIMEMultipart('alternative')

        msg['Subject'] = 'Bitcoinsnotification!'
        msg['From'] = 'Daniel Bastos <danielfloresbastos@gmail.com>'
        msg['To'] = 'danielfloresbastos@gmail.com'

        text = 'Valor do Bitcoin | ask: {0} bid: {1}'.format(data['ask'], data['bid'])
        part = MIMEText(text, 'plain')
        username = 'danielfloresbastos@gmail.com'  # os.environ['MANDRILL_USERNAME']
        password = 'QjJ9weB49OIq_xu9vLrtcQ'  # os.environ['MANDRILL_PASSWORD']
        msg.attach(part)

        s = smtplib.SMTP('smtp.mandrillapp.com', 587)
        s.login(username, password)
        s.sendmail(msg['From'], msg['To'], msg.as_string())

        s.quit()
    """
