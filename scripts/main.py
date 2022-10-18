import os, sys
sys.path.insert(0, os.getcwd())

from arango import ArangoClient
from hashlib import sha256
from dotenv import load_dotenv
load_dotenv()

BOOK_1 = os.getenv('BOOK_1')
BOOK_2 = os.getenv('BOOK_2')
BOOK_3 = os.getenv('BOOK_3')
BOOK_4 = os.getenv('BOOK_4')
BOOK_5 = os.getenv('BOOK_5')
BOOK_6 = os.getenv('BOOK_6')
BOOK_7 = os.getenv('BOOK_7')
BOOK_8 = os.getenv('BOOK_8')
BOOK_9 = os.getenv('BOOK_9')
BOOK_10 = os.getenv('BOOK_10')

from src.constants import EDGE_COLLECTION, URL_ARANGO_DB, DB_NAME, NODE_COLLECTION, SEPARATOR, WORDS_GRAPH
from src.functions import most_likely_path, random_word_sample, read_txt, find_word, recommend


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

    counted_words, following_words = read_txt([BOOK_1, BOOK_2, BOOK_3, BOOK_4, BOOK_5, BOOK_6, BOOK_7, BOOK_8, BOOK_9, BOOK_10])

    # Add nodes
    inserted_nodes = 0
    for key, value in counted_words.items():
        words.insert({
            "_key": sha256(key.encode()).hexdigest(),
            "name": key,
            "count": value
        })
        inserted_nodes += 1
        if(inserted_nodes % 10 == 0):
            print("Inserted " + str(inserted_nodes) + " nodes")

    # Add edges
    inserted_edges = 0
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
        inserted_edges += 1
        if(inserted_edges % 10 == 0):
            print("Inserted " + str(inserted_edges) + " edges")

    print("Creando grafo de palabras relacionadas...")
    related_words_graph = db.create_graph(WORDS_GRAPH)

    if not related_words_graph.has_edge_definition(EDGE_COLLECTION):
        related_words_graph.create_edge_definition(EDGE_COLLECTION, [NODE_COLLECTION], [NODE_COLLECTION])

    print("Finished populating database: " + DB_NAME)

else:
    db = client.db(DB_NAME, username="root")
    related_words_graph = db.graph(WORDS_GRAPH)
    print("Database already exists: " + DB_NAME)

finded_word = find_word(db.aql, 'hola')
second_finded_word = find_word(db.aql, 'que')
print('Probando 1: ' + finded_word['name'] + ' ' + second_finded_word['name'])

print(most_likely_path(db.aql, finded_word['_id'], second_finded_word['_id']))

finded_word = find_word(db.aql, 'buenas')
print('Probando 2: ' + finded_word['name'])
print(recommend(related_words_graph, finded_word['_key']))

sit = find_word(db.aql, 'entonces')
print('Probando 3: ' + sit['name'])
print(random_word_sample(related_words_graph, sit['_key'])) 
client.close()