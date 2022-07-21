import os, sys
sys.path.insert(0, os.getcwd())

from arango import ArangoClient
from hashlib import sha256

from src.constants import EDGE_COLLECTION, URL_ARANGO_DB, DB_NAME, NODE_COLLECTION, SEPARATOR
from src.functions import readTxt

# Initialize the client for ArangoDB.
client = ArangoClient(hosts=URL_ARANGO_DB)
db = client.db(DB_NAME, username="root")
words = db.collection(NODE_COLLECTION)
follows = db.collection(EDGE_COLLECTION)

#Why it is not working with relative paths?
counted_words, following_words = readTxt('C:/Users/Alberto_Work/Desktop/TFG/bachelorThesis/books/loremIpsun.txt')

# Add nodes
for key, value in counted_words.items():
    words.insert({
        "_key": sha256(key.encode()).hexdigest(),
        "name": key,
        "count": value
    })

# Add edges
for key, value in following_words.items():
    for key2, value2 in value.items():
        follows.insert({
            "_key": sha256((key + SEPARATOR + key2).encode()).hexdigest(),
            "_from": NODE_COLLECTION + '/' + sha256(key.encode()).hexdigest(),
            "_to": NODE_COLLECTION + '/' + sha256(key2.encode()).hexdigest(),
            "count": value2
        })
        
print("Finished populating database: " + DB_NAME)