from arango import ArangoClient
from src.constants import URL_ARANGO_DB, DB_NAME, NODE_COLLECTION
from src.functions import readTxt

# Initialize the client for ArangoDB.
client = ArangoClient(hosts=URL_ARANGO_DB)
db = client.db(DB_NAME, username="root")
words = db.collection(NODE_COLLECTION)

#Why it is not working with relative paths?
counted_words = readTxt('C:/Users/Alberto_Work/Desktop/TFG/finalGradeProject/books/loremIpsun.txt') 

for key, value in counted_words.items():
    words.insert({
        "name": key,
        "count": value
    })

print("Finished populating database: " + DB_NAME)