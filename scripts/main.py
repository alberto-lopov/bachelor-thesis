import os, sys
sys.path.insert(0, os.getcwd())

from arango import ArangoClient
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

from src.constants import TOTAL_COLLECTIONS, URL_ARANGO_DB, DB_NAME
from src.functions import bigram_initialization, find_ngram, main_menu, phrase_suggestions, read_txt, trigram_initialization, unigram_initialization

# Initialize the client for ArangoDB.
client = ArangoClient(hosts=URL_ARANGO_DB)
sys_db = client.db("_system", username="root")
db = None

#Initializate ArangoDB words_database if it doesn't exist
if not sys_db.has_database(DB_NAME):
    sys_db.create_database(DB_NAME)
    print("Se ha creado la base de datos: " + DB_NAME)

# Connect to database as root user.
db = client.db(DB_NAME, username="root")
print("Conectado a la base de datos: " + DB_NAME)

# -- Populate database / Training of model in case it hasn't been done --
if len(db.collections()) < TOTAL_COLLECTIONS:
    uni_words, uni_follows, bi_words, bi_follows, tri_words, tri_follows = read_txt(
        [BOOK_1, BOOK_2, BOOK_3, BOOK_4, BOOK_5, BOOK_6, BOOK_7, BOOK_8, BOOK_9, BOOK_10, BOOK_11, BOOK_12, BOOK_13, BOOK_14]
    )

    unigram_initialization(db, uni_words, uni_follows)
    bigram_initialization(db, bi_words, bi_follows)
    trigram_initialization(db, tri_words, tri_follows)

#main_menu(db)
print(phrase_suggestions(db))
"""
related_words_graph = db.graph(UNI_WORDS_GRAPH)
finded_word = find_ngram(db, 'hola')
print(finded_word)
second_finded_word = find_ngram(db, 'tal')
print('Probando 1: ' + finded_word['name'] + ' ' + second_finded_word['name'])

print(path_given_two_words(db.aql, finded_word['_id'], second_finded_word['_id']))

finded_word = find_ngram(db, 'buenas')
print('Probando 2: ' + finded_word['name'])
print(recommend_ngram_list(related_words_graph, finded_word['_key']))

sit = find_ngram(db, 'entonces')
print('Probando 3: ' + sit['name'])
print(random_word_sample(related_words_graph, sit['_key']))"""

client.close()