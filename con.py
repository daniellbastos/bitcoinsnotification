import os
from pymongo import MongoClient

dbhost = os.environ.get('OPENSHIFT_MONGODB_DB_HOST', 'localhost')
dbport = os.environ.get('OPENSHIFT_MONGODB_DB_PORT', 27017)
dbuser = os.environ.get('OPENSHIFT_MONGODB_DB_USERNAME', None)
dbpass = os.environ.get('OPENSHIFT_MONGODB_DB_PASSWORD', None)

if dbuser:
    uri = 'mongodb://{0}:{1}@{2}:{3}/bitcoinsnotification'.format(
        dbuser, dbpass, dbhost, dbport)
else:
    uri = 'mongodb://{0}:{1}/bitcoinsnotification'.format(dbhost, dbport)

client = MongoClient(uri)
db = client.get_default_database()

foxbit = db['foxbit']
contact = db['contact']
