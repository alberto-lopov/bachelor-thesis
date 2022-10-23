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
BOOK_11 = os.getenv('BOOK_11')
BOOK_12 = os.getenv('BOOK_12')
BOOK_13 = os.getenv('BOOK_13')
BOOK_14 = os.getenv('BOOK_14')

from src.constants import BI_EDGE_COLLECTION, BI_NODE_COLLECTION, TRI_EDGE_COLLECTION, TRI_NODE_COLLECTION, UNI_EDGE_COLLECTION, URL_ARANGO_DB, DB_NAME, UNI_NODE_COLLECTION, UNI_WORDS_GRAPH
from src.functions import bigram_insertion, most_likely_path, random_word_sample, read_txt, find_word, recommend, trigram_insertion, unigram_insertion


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

    # Create node collections and add a fulltext index to collection
    (db.create_collection(UNI_NODE_COLLECTION)).add_fulltext_index(fields=["name"])
    (db.create_collection(BI_NODE_COLLECTION)).add_fulltext_index(fields=["name"])
    (db.create_collection(TRI_NODE_COLLECTION)).add_fulltext_index(fields=["name"])
    
    # Create edge collections
    db.create_collection(UNI_EDGE_COLLECTION, edge=True)
    db.create_collection(BI_EDGE_COLLECTION, edge=True)
    db.create_collection(TRI_EDGE_COLLECTION, edge=True)

    print("Finished creating database: " + DB_NAME)

    # -- Populate database / Training of model --
    uni_words, uni_follows, bi_words, bi_follows, tri_words, tri_follows = read_txt(
        [BOOK_1, BOOK_2, BOOK_3, BOOK_4, BOOK_5, BOOK_6, BOOK_7, BOOK_8, BOOK_9, BOOK_10, BOOK_11, BOOK_12, BOOK_13, BOOK_14]
    )

    unigram_insertion(db, uni_words, uni_follows)
    bigram_insertion(db, bi_words, bi_follows)
    trigram_insertion(db, tri_words, tri_follows)
    
    print("Finished populating database: " + DB_NAME)

else:
    db = client.db(DB_NAME, username="root")
    related_words_graph = db.graph(UNI_WORDS_GRAPH)
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