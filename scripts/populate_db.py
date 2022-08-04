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

# Create graph
if db.has_graph('relatedWords'):
    related_words_graph = db.graph('relatedWords')
else:
    related_words_graph = db.create_graph('relatedWords')

if not related_words_graph.has_edge_definition(EDGE_COLLECTION):
    related_words_graph.create_edge_definition(EDGE_COLLECTION, [NODE_COLLECTION], [NODE_COLLECTION])

# 1 modo de predicion: Funcion para recomendar siguiente palabra dada una palabra
def recommend(self, text: str) -> List[dict]:
        tokenList = self.getTokenList(text)
        tokenList = self.standardize(tokenList)
        if len(tokenList) >= self.ngramFrom:
            _from: str = self.joinStr.join(tokenList[-self.ngramFrom:])
            keyHash: str = hashlib.md5(_from.encode()).hexdigest()
            nodeCollection: str = self.getVertexCollectionName()
            paths = self.graph.traverse(
                start_vertex = nodeCollection + "/" + keyHash,
                direction = "outbound",
                strategy = "bfs",
                min_depth = 1,
                max_depth = 1
            )["paths"] # return lista de palabras conectadas, con longitud maxima de 1
            
            # ordenar los ejes porcampoinverso y sacar la mas frecuentes
            edges = [path["edges"][0] for path in paths]  
            return list(sorted([
                {
                    "token": edge["to"].split("/")[1],
                    "count": edge["count"],
                    "ngramFrom": edge["ngramFrom"],
                    "ngramTo": edge["ngramTo"],
                    "value": edge["count"] * edge["ngramFrom"] * edge["ngramTo"]
                } 
            for edge in edges], key = lambda x: x["value"], reverse = True))
        return []

#2 modo de predicion query para devolver el camino más probable entre dos palabras (el camino de maxima probabilidad)
query = """
    FOR v, e IN OUTBOUND SHORTEST_PATH '{origin}' TO '{goal}' 
        GRAPH 'graph' 
        OPTIONS {
            weightAttribute: 'inverse_count',
            defaultWeight: 0
        }
        RETURN [v._key,v.lat,v.lon,e._key,e.inverse_count]
"""

#sustituyendolo
"""FOR v, e IN OUTBOUND SHORTEST_PATH 'words/1b7f8466f087c27f24e1c90017b829cd8208969018a0bbe7d9c452fa224bc6cc' TO 'words/8e317f8df6bcc28e25cc1bf9aa449d68679ce17b53a0cb2b2cfce188031380dc' 
        GRAPH 'relatedWords' 
        OPTIONS {
            weightAttribute: 'count',
            defaultWeight: 0
        }
        RETURN [v._key,v.name,e._key,e.count]"""
    
#3 modo de predicion
#~hay que hacer algo donde se importe de scipy import stats
print("Finished populating database: " + DB_NAME)