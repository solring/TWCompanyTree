import json
from pymongo import MongoClient
from sys import argv

if len(argv) < 3:
    print "usage: python import_mongodb.py [username:password@host:port] [collection] [file name]"
    exit(0)

url = 'mongodb://'+argv[1]
col_name = argv[2]
	
# read import file
with open(argv[3], "r") as fd:
	data = json.load(fd, encoding='utf-8') # parse array into array object
	
	print 'connecting to '+argv[1]+'......'
	client = MongoClient(url)
	if client == None:
		print 'connection failed.'
		exit(0)

	db = client['TWcompany']
	collection = db[col_name]
	collection.insert(data)

	client.close()

