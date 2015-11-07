import os
from pymongo import MongoClient

dburl = os.environ.get('OPENSHIFT_MONGODB_DB_URL', None)
if not dburl:
    dburl = 'mongodb://localhost:27017/'
dburl += 'bitcoinsnotification'

client = MongoClient(dburl, tz_aware=True)
db = client.get_default_database()

foxbit = db['foxbit']
contact = db['contact']
