import json
from urllib import request
from datetime import datetime
from con import mongolab

url = 'https://api.bitcoinaverage.com/ticker/global/BRL/'
resp = request.urlopen(url).read()
data = json.loads(resp.decode('utf-8'))
data['timestamp'] = datetime.now()
data['daily_avg'] = data['24h_avg']

mongolab.insert(data)
