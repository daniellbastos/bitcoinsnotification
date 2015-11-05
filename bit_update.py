import json
from urllib import request
from datetime import datetime
from con import mongolab


def bitcoinaverage():
    url = 'https://api.bitcoinaverage.com/ticker/global/BRL/'
    resp = request.urlopen(url).read()
    data = json.loads(resp.decode('utf-8'))
    data['timestamp'] = datetime.utcnow()
    data['daily_avg'] = data['24h_avg']
    mongolab.insert(data)

    if data['ask'] <= 1600 or data['bid'] <= 1600:
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
