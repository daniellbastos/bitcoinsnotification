from pymongo import MongoClient

uri = 'mongodb://{0}:{0}@ds049864.mongolab.com:49864/bitcoinsnotification'
uri = uri.format('bitcoinsnotification')
client = MongoClient(
    uri, connectTimeoutMS=30000, socketTimeoutMS=None, socketKeepAlive=True)
db = client.get_default_database()
mongolab = db['bitcoinsnotification']
contact = db['contact']
