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
from src.functions.database_interaction import  bigram_char_init, bigram_word_init, trigram_char_init, trigram_word_init, unigram_char_init, unigram_word_init
from src.functions.features import main_menu
from src.functions.reader import read_txt

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
    uni_words, uni_follows, bi_words, bi_follows, tri_words, tri_follows, uni_chars, uni_char_follows, bi_chars, bi_char_follows, tri_chars, tri_char_follows = read_txt(
        [BOOK_1, BOOK_2, BOOK_3, BOOK_4, BOOK_5, BOOK_6, BOOK_7, BOOK_8, BOOK_9, BOOK_10, BOOK_11, BOOK_12, BOOK_13, BOOK_14]
    )

    unigram_word_init(db, uni_words, uni_follows)
    unigram_char_init(db, uni_chars, uni_char_follows)
    bigram_word_init(db, bi_words, bi_follows)
    bigram_char_init(db, bi_chars, bi_char_follows)
    trigram_word_init(db, tri_words, tri_follows)
    trigram_char_init(db, tri_chars, tri_char_follows)

main_menu(db)

client.close()