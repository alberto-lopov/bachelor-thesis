# This currently only works when executed with python -m scripts.init_db

from arango import ArangoClient
from src.constants import URL_ARANGO_DB, DB_NAME, NODE_COLLECTION, EDGE_COLLECTION

# Initialize the client for ArangoDB.
client = ArangoClient(hosts=URL_ARANGO_DB)

# Connect to "_system" database as root user.
sys_db = client.db("_system", username="root")

# Create a new database
if not sys_db.has_database(DB_NAME):
    sys_db.create_database(DB_NAME)

    # Connect to new database as root user.
    db = client.db(DB_NAME, username="root")

    # Create a new collections.
    words = db.create_collection(NODE_COLLECTION)
    db.create_collection(EDGE_COLLECTION, edge=True)

    # Add a hash index to the collection.
    words.add_fulltext_index(fields=["name"])

    print("Finished creating database: " + DB_NAME)

else:
    print("Database already exists: " + DB_NAME)

client.close()