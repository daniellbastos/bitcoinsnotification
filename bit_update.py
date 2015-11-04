from urllib import request
from pymongo import MongoClient
from datetime import datetime

import json

uri = 'mongodb://{0}:{0}@ds049864.mongolab.com:49864/bitcoinsnotification'
uri = uri.format('bitcoinsnotification')
client = MongoClient(
    uri, connectTimeoutMS=30000, socketTimeoutMS=None, socketKeepAlive=True)
db = client.get_default_database()
mongolab = db['bitcoinsnotification']

url = 'https://api.bitcoinaverage.com/ticker/global/BRL/'
resp = request.urlopen(url).read()
data = json.loads(resp.decode('utf-8'))
data['timestamp'] = datetime.now()

mongolab.insert(data)
