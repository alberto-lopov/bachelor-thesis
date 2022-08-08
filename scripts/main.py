import os, sys
sys.path.insert(0, os.getcwd())

from arango import ArangoClient
from hashlib import sha256
from dotenv import load_dotenv
load_dotenv()
LOREM_BOOK = os.getenv('LOREM_BOOK')

from src.constants import EDGE_COLLECTION, URL_ARANGO_DB, DB_NAME, NODE_COLLECTION, SEPARATOR, WORDS_GRAPH
from src.functions import most_likely_path, read_txt, find_word, recommend


# Initialize the client for ArangoDB.
client = ArangoClient(hosts=URL_ARANGO_DB)
sys_db = client.db("_system", username="root")
db = None
related_words_graph = None

#Initializate ArangoDB words_database if it doesn't exist
if not sys_db.has_database(DB_NAME):
    sys_db.create_database(DB_NAME)

    # Connect to new database as root user.
    db = client.db(DB_NAME, username="root")

    # Create a new collections.
    collection = db.create_collection(NODE_COLLECTION)
    db.create_collection(EDGE_COLLECTION, edge=True)

    # Add a hash index to the collection.
    collection.add_fulltext_index(fields=["name"])

    print("Finished creating database: " + DB_NAME)

    # -- Populate database / Training of model --
    words = db.collection(NODE_COLLECTION)
    follows = db.collection(EDGE_COLLECTION)

    counted_words, following_words = read_txt(LOREM_BOOK)

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
                "count": value2,
                "from_name": key,
                "to_name": key2,
                "inverse_count": 1/value2
            })

    related_words_graph = db.create_graph(WORDS_GRAPH)

    if not related_words_graph.has_edge_definition(EDGE_COLLECTION):
        related_words_graph.create_edge_definition(EDGE_COLLECTION, [NODE_COLLECTION], [NODE_COLLECTION])

    print("Finished populating database: " + DB_NAME)

else:
    db = client.db(DB_NAME, username="root")
    related_words_graph = db.graph(WORDS_GRAPH)
    print("Database already exists: " + DB_NAME)

lorem = find_word(db.aql, 'Lorem')
consectetur = find_word(db.aql, 'consectetur')
print('Probando: ' + lorem['name'] + ' ' + consectetur['name'])

print(most_likely_path(db.aql, lorem['_id'], consectetur['_id']))

lorem = find_word(db.aql, 'lorem')
print('Probando: ' + lorem['name'])
print(recommend(related_words_graph, lorem['_key']))
client.close()