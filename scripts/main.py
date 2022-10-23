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

from src.constants import BI_EDGE_COLLECTION, BI_NODE_COLLECTION, BI_WORDS_GRAPH, TRI_EDGE_COLLECTION, TRI_NODE_COLLECTION, TRI_WORDS_GRAPH, UNI_EDGE_COLLECTION, URL_ARANGO_DB, DB_NAME, UNI_NODE_COLLECTION, EDGE_SEPARATOR, UNI_WORDS_GRAPH, WORD_SEPARATOR
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
    words = db.collection(UNI_NODE_COLLECTION)
    follows = db.collection(UNI_EDGE_COLLECTION)

    uni_words, uni_follows, bi_words, bi_follows, tri_words, tri_follows = read_txt([BOOK_1, BOOK_2, BOOK_3, BOOK_4, BOOK_5, BOOK_6, BOOK_7, BOOK_8, BOOK_9, BOOK_10])

    # --- Create graphs
    # Add nodes
    inserted_nodes = 0
    for key, value in uni_words.items():
        words.insert({
            "_key": sha256(key.encode()).hexdigest(),
            "name": key,
            "count": value
        })
        inserted_nodes += 1
        if(inserted_nodes % 10 == 0):
            print("Inserted " + str(inserted_nodes) + " UNIGRAM nodes")

    # Add edges
    inserted_edges = 0
    for key, value in uni_follows.items():
        for key2, value2 in value.items():
            follows.insert({
                "_key": sha256((key + EDGE_SEPARATOR + key2).encode()).hexdigest(),
                "_from": UNI_NODE_COLLECTION + '/' + sha256(key.encode()).hexdigest(),
                "_to": UNI_NODE_COLLECTION + '/' + sha256(key2.encode()).hexdigest(),
                "count": value2,
                "from_name": key,
                "to_name": key2,
                "inverse_count": 1/value2
            })
        inserted_edges += 1
        if(inserted_edges % 10 == 0):
            print("Inserted " + str(inserted_edges) + " UNIGRAM edges")

    print("Creado grafo de UNIGRAMAS")
    related_words_graph = db.create_graph(UNI_WORDS_GRAPH)

    if not related_words_graph.has_edge_definition(UNI_EDGE_COLLECTION):
        related_words_graph.create_edge_definition(UNI_EDGE_COLLECTION, [UNI_NODE_COLLECTION], [UNI_NODE_COLLECTION])

    bi_node = db.collection(BI_NODE_COLLECTION)
    bi_edge = db.collection(BI_EDGE_COLLECTION)

    # Add nodes
    inserted_nodes = 0
    for key, value in bi_words.items():
        bi_node.insert({
            "_key": sha256(key.encode()).hexdigest(),
            "name": key.replace(WORD_SEPARATOR, " "),
            "first": key.split(WORD_SEPARATOR)[0],
            "second": key.split(WORD_SEPARATOR)[1],
            "count": value
        })
        inserted_nodes += 1
        if(inserted_nodes % 10 == 0):
            print("Inserted " + str(inserted_nodes) + " BIGRAM nodes")

    # Add edges
    inserted_edges = 0
    for key, value in bi_follows.items():
        for key2, value2 in value.items():
            bi_edge.insert({
                "_key": sha256((key + EDGE_SEPARATOR + key2).encode()).hexdigest(),
                "_from": BI_NODE_COLLECTION + '/' + sha256(key.encode()).hexdigest(),
                "_to": BI_NODE_COLLECTION + '/' + sha256(key2.encode()).hexdigest(),
                "count": value2,
                "from_name": key.replace(WORD_SEPARATOR, " "),
                "to_name": key2.replace(WORD_SEPARATOR, " "),
                "inverse_count": 1/value2
            })
        inserted_edges += 1
        if(inserted_edges % 10 == 0):
            print("Inserted " + str(inserted_edges) + " BIGRAM edges")

    print("Creando grafo de BIGRAMAS.")
    bi_words_graph = db.create_graph(BI_WORDS_GRAPH)

    if not bi_words_graph.has_edge_definition(BI_EDGE_COLLECTION):
        bi_words_graph.create_edge_definition(BI_EDGE_COLLECTION, [BI_NODE_COLLECTION], [BI_NODE_COLLECTION])
    
    tri_node = db.collection(TRI_NODE_COLLECTION)
    tri_edge = db.collection(TRI_EDGE_COLLECTION)

    # Add nodes
    inserted_nodes = 0
    for key, value in tri_words.items():
        tri_node.insert({
            "_key": sha256(key.encode()).hexdigest(),
            "name": key.replace(WORD_SEPARATOR, " "),
            "first": key.split(WORD_SEPARATOR)[0],
            "second": key.split(WORD_SEPARATOR)[1],
            "third": key.split(WORD_SEPARATOR)[2],
            "count": value
        })
        inserted_nodes += 1
        if(inserted_nodes % 10 == 0):
            print("Inserted " + str(inserted_nodes) + " TRIGRAM nodes")

    # Add edges
    inserted_edges = 0
    for key, value in tri_follows.items():
        for key2, value2 in value.items():
            tri_edge.insert({
                "_key": sha256((key + EDGE_SEPARATOR + key2).encode()).hexdigest(),
                "_from": BI_NODE_COLLECTION + '/' + sha256(key.encode()).hexdigest(),
                "_to": BI_NODE_COLLECTION + '/' + sha256(key2.encode()).hexdigest(),
                "count": value2,
                "from_name": key.replace(WORD_SEPARATOR, " "),
                "to_name": key2.replace(WORD_SEPARATOR, " "),
                "inverse_count": 1/value2
            })
        inserted_edges += 1
        if(inserted_edges % 10 == 0):
            print("Inserted " + str(inserted_edges) + " TRIGRAM edges")

    print("Creando grafo de TRIGRAMAS")
    tri_words_graph = db.create_graph(TRI_WORDS_GRAPH)

    if not tri_words_graph.has_edge_definition(TRI_EDGE_COLLECTION):
        tri_words_graph.create_edge_definition(TRI_EDGE_COLLECTION, [TRI_NODE_COLLECTION], [TRI_NODE_COLLECTION])
    
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