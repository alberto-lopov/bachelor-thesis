from hashlib import sha256
from scipy.stats import rv_discrete
from typing import List

from src.constants import BI_CHAR_EDGE, BI_CHAR_NODE, BI_CHARS_GRAPH, BI_WORD_EDGE, BI_WORD_NODE, BI_WORDS_GRAPH, EDGE_SEPARATOR, GRAPH_TO_COLLECTION, GRAPH_TO_OPTION, NODE_SEPARATOR, TRI_CHAR_EDGE, TRI_CHAR_NODE, TRI_CHARS_GRAPH, TRI_WORD_EDGE, TRI_WORD_NODE, TRI_WORDS_GRAPH, UNI_CHAR_EDGE, UNI_CHAR_NODE, UNI_CHARS_GRAPH, UNI_WORD_EDGE, UNI_WORD_NODE, UNI_WORDS_GRAPH

# ---------------------------------------------------------- DATA INSERTION FUNCTIONS ----------------------------------------------------------

def unigram_word_init(db, uni_words, uni_follows):
	
	# Add nodes
	if not db.has_collection(UNI_WORD_NODE):
		words = db.create_collection(UNI_WORD_NODE)
		words.add_fulltext_index(fields=["name"])
		
		inserted_nodes = 0
		for key, value in uni_words.items():
			words.insert({
				"_key": sha256(key.encode()).hexdigest(),
				"name": key,
				"count": value
			})
			inserted_nodes += 1
			if(inserted_nodes % 1000 == 0):
				print("Insertados " + str(inserted_nodes) + " nodos de palabras - UNIGRAMAS")

	# Add edges
	if not db.has_collection(UNI_WORD_EDGE):
		follows = db.create_collection(UNI_WORD_EDGE, edge=True)
		
		inserted_edges = 0
		for key, value in uni_follows.items():
			for key2, value2 in value.items():
				follows.insert({
					"_key": sha256((key + EDGE_SEPARATOR + key2).encode()).hexdigest(),
					"_from": UNI_WORD_NODE + '/' + sha256(key.encode()).hexdigest(),
					"_to": UNI_WORD_NODE + '/' + sha256(key2.encode()).hexdigest(),
					"count": value2,
					"from_name": key,
					"to_name": key2,
					"inverse_count": 1/value2
				})
			inserted_edges += 1
			if(inserted_edges % 10 == 0):
				print("Insertados " + str(inserted_edges) + " arcos de palabras - UNIGRAMAS")

	# --- Create graphs
	if not db.has_graph(UNI_WORDS_GRAPH):
		related_words_graph = db.create_graph(UNI_WORDS_GRAPH)
		print("Creado grafo de palabras - UNIGRAMAS")

		if not related_words_graph.has_edge_definition(UNI_WORD_EDGE):
			related_words_graph.create_edge_definition(UNI_WORD_EDGE, [UNI_WORD_NODE], [UNI_WORD_NODE])

def unigram_char_init(db, uni_chars, uni_char_follows):
	
	# Add nodes
	if not db.has_collection(UNI_CHAR_NODE):
		chars = db.create_collection(UNI_CHAR_NODE)
		chars.add_fulltext_index(fields=["name"])
		
		inserted_nodes = 0
		for key, value in uni_chars.items():
			chars.insert({
				"_key": sha256(key.encode()).hexdigest(),
				"name": key,
				"count": value
			})
			inserted_nodes += 1
			if(inserted_nodes % 10 == 0):
				print("Insertados " + str(inserted_nodes) + " nodos de caracteres - UNIGRAMAS")

	# Add edges
	if not db.has_collection(UNI_CHAR_EDGE):
		char_follows = db.create_collection(UNI_CHAR_EDGE, edge=True)
		
		inserted_edges = 0
		for key, value in uni_char_follows.items():
			for key2, value2 in value.items():
				char_follows.insert({
					"_key": sha256((key + EDGE_SEPARATOR + key2).encode()).hexdigest(),
					"_from": UNI_CHAR_NODE + '/' + sha256(key.encode()).hexdigest(),
					"_to": UNI_CHAR_NODE + '/' + sha256(key2.encode()).hexdigest(),
					"count": value2,
					"from_name": key,
					"to_name": key2,
					"inverse_count": 1/value2
				})
			inserted_edges += 1
			if(inserted_edges % 10 == 0):
				print("Insertados " + str(inserted_edges) + " arcos de caracteres - UNIGRAMAS")

	# --- Create graphs
	if not db.has_graph(UNI_CHARS_GRAPH):
		related_words_graph = db.create_graph(UNI_CHARS_GRAPH)
		print("Creado grafo de caracteres - UNIGRAMAS")

		if not related_words_graph.has_edge_definition(UNI_CHAR_EDGE):
			related_words_graph.create_edge_definition(UNI_CHAR_EDGE, [UNI_CHAR_NODE], [UNI_CHAR_NODE])

def bigram_word_init(db, bi_words, bi_follows):
	
	# Add nodes
	if not db.has_collection(BI_WORD_NODE):
		bi_node = db.create_collection(BI_WORD_NODE)
		bi_node.add_fulltext_index(fields=["name"])

		inserted_nodes = 0
		for key, value in bi_words.items():
			bi_node.insert({
				"_key": sha256(key.encode()).hexdigest(),
				"name": key.replace(NODE_SEPARATOR, " "),
				"first": key.split(NODE_SEPARATOR)[0],
				"second": key.split(NODE_SEPARATOR)[1],
				"count": value
			})
			inserted_nodes += 1
			if(inserted_nodes % 1000 == 0):
				print("Insertados " + str(inserted_nodes) + " nodos de palabras - BIGRAMAS")

	# Add edges
	if not db.has_collection(BI_WORD_EDGE):
		bi_edge = db.create_collection(BI_WORD_EDGE, edge=True)
		
		inserted_edges = 0
		for key, value in bi_follows.items():
			for key2, value2 in value.items():
				bi_edge.insert({
					"_key": sha256((key + EDGE_SEPARATOR + key2).encode()).hexdigest(),
					"_from": BI_WORD_NODE + '/' + sha256(key.encode()).hexdigest(),
					"_to": BI_WORD_NODE + '/' + sha256(key2.encode()).hexdigest(),
					"count": value2,
					"from_name": key.replace(NODE_SEPARATOR, " "),
					"to_name": key2.replace(NODE_SEPARATOR, " "),
					"inverse_count": 1/value2
				})
			inserted_edges += 1
			if(inserted_edges % 10 == 0):
				print("Insertados " + str(inserted_edges) + " arcos de palabras - BIGRAMAS")

	if not db.has_graph(BI_WORDS_GRAPH):
		bi_words_graph = db.create_graph(BI_WORDS_GRAPH)
		print("Creado grafo de palabras - BIGRAMAS.")

		if not bi_words_graph.has_edge_definition(BI_WORD_EDGE):
			bi_words_graph.create_edge_definition(BI_WORD_EDGE, [BI_WORD_NODE], [BI_WORD_NODE])

def bigram_char_init(db, bi_chars, bi_char_follows):
	
	# Add nodes
	if not db.has_collection(BI_CHAR_NODE):
		bi_node = db.create_collection(BI_CHAR_NODE)
		bi_node.add_fulltext_index(fields=["name"])

		inserted_nodes = 0
		for key, value in bi_chars.items():
			bi_node.insert({
				"_key": sha256(key.encode()).hexdigest(),
				"name": key.replace(NODE_SEPARATOR, ""),
				"first": key.split(NODE_SEPARATOR)[0],
				"second": key.split(NODE_SEPARATOR)[1],
				"count": value
			})
			inserted_nodes += 1
			if(inserted_nodes % 10 == 0):
				print("Insertados " + str(inserted_nodes) + " nodos de caracteres - BIGRAMAS")

	# Add edges
	if not db.has_collection(BI_CHAR_EDGE):
		bi_edge = db.create_collection(BI_CHAR_EDGE, edge=True)
		
		inserted_edges = 0
		for key, value in bi_char_follows.items():
			for key2, value2 in value.items():
				bi_edge.insert({
					"_key": sha256((key + EDGE_SEPARATOR + key2).encode()).hexdigest(),
					"_from": BI_CHAR_NODE + '/' + sha256(key.encode()).hexdigest(),
					"_to": BI_CHAR_NODE + '/' + sha256(key2.encode()).hexdigest(),
					"count": value2,
					"from_name": key.replace(NODE_SEPARATOR, ""),
					"to_name": key2.replace(NODE_SEPARATOR, ""),
					"inverse_count": 1/value2
				})
			inserted_edges += 1
			if(inserted_edges % 10 == 0):
				print("Insertados " + str(inserted_edges) + " arcos de caracteres - BIGRAMAS")

	if not db.has_graph(BI_CHARS_GRAPH):
		bi_words_graph = db.create_graph(BI_CHARS_GRAPH)
		print("Creado grafo de caracteres - BIGRAMAS.")

		if not bi_words_graph.has_edge_definition(BI_CHAR_EDGE):
			bi_words_graph.create_edge_definition(BI_CHAR_EDGE, [BI_CHAR_NODE], [BI_CHAR_NODE])

def trigram_word_init(db, tri_words, tri_follows):
	
	# Add nodes
	if not db.has_collection(TRI_WORD_NODE):
		tri_node = db.create_collection(TRI_WORD_NODE)
		tri_node.add_fulltext_index(fields=["name"])

		inserted_nodes = 0
		for key, value in tri_words.items():
			tri_node.insert({
				"_key": sha256(key.encode()).hexdigest(),
				"name": key.replace(NODE_SEPARATOR, " "),
				"first": key.split(NODE_SEPARATOR)[0],
				"second": key.split(NODE_SEPARATOR)[1],
				"third": key.split(NODE_SEPARATOR)[2],
				"count": value
			})
			inserted_nodes += 1
			if(inserted_nodes % 1000 == 0):
				print("Insertados " + str(inserted_nodes) + " nodos de palabras - TRIGRAMAS")

	# Add edges
	if not db.has_collection(TRI_WORD_EDGE):
		tri_edge = db.create_collection(TRI_WORD_EDGE, edge=True)
		inserted_edges = 0
		for key, value in tri_follows.items():
			for key2, value2 in value.items():
				tri_edge.insert({
					"_key": sha256((key + EDGE_SEPARATOR + key2).encode()).hexdigest(),
					"_from": TRI_WORD_NODE + '/' + sha256(key.encode()).hexdigest(),
					"_to": TRI_WORD_NODE + '/' + sha256(key2.encode()).hexdigest(),
					"count": value2,
					"from_name": key.replace(NODE_SEPARATOR, " "),
					"to_name": key2.replace(NODE_SEPARATOR, " "),
					"inverse_count": 1/value2
				})
			inserted_edges += 1
			if(inserted_edges % 10 == 0):
				print("Insertados " + str(inserted_edges) + " arcos de palabras - TRIGRAMAS")

	if not db.has_graph(TRI_WORDS_GRAPH):
		tri_words_graph = db.create_graph(TRI_WORDS_GRAPH)
		print("Creado grafo de palabras - TRIGRAMAS")

		if not tri_words_graph.has_edge_definition(TRI_WORD_EDGE):
			tri_words_graph.create_edge_definition(TRI_WORD_EDGE, [TRI_WORD_NODE], [TRI_WORD_NODE])

def trigram_char_init(db, tri_chars, tri_char_follows):
	
	# Add nodes
	if not db.has_collection(TRI_CHAR_NODE):
		tri_node = db.create_collection(TRI_CHAR_NODE)
		tri_node.add_fulltext_index(fields=["name"])

		inserted_nodes = 0
		for key, value in tri_chars.items():
			tri_node.insert({
				"_key": sha256(key.encode()).hexdigest(),
				"name": key.replace(NODE_SEPARATOR, ""),
				"first": key.split(NODE_SEPARATOR)[0],
				"second": key.split(NODE_SEPARATOR)[1],
				"third": key.split(NODE_SEPARATOR)[2],
				"count": value
			})
			inserted_nodes += 1
			if(inserted_nodes % 1000 == 0):
				print("Insertados " + str(inserted_nodes) + " nodos de caracteres - TRIGRAMAS")

	# Add edges
	if not db.has_collection(TRI_CHAR_EDGE):
		tri_edge = db.create_collection(TRI_CHAR_EDGE, edge=True)
		inserted_edges = 0
		for key, value in tri_char_follows.items():
			for key2, value2 in value.items():
				tri_edge.insert({
					"_key": sha256((key + EDGE_SEPARATOR + key2).encode()).hexdigest(),
					"_from": TRI_CHAR_NODE + '/' + sha256(key.encode()).hexdigest(),
					"_to": TRI_CHAR_NODE + '/' + sha256(key2.encode()).hexdigest(),
					"count": value2,
					"from_name": key.replace(NODE_SEPARATOR, ""),
					"to_name": key2.replace(NODE_SEPARATOR, ""),
					"inverse_count": 1/value2
				})
			inserted_edges += 1
			if(inserted_edges % 10 == 0):
				print("Insertados " + str(inserted_edges) + " arcos de caracteres - TRIGRAMAS")

	if not db.has_graph(TRI_CHARS_GRAPH):
		tri_words_graph = db.create_graph(TRI_CHARS_GRAPH)
		print("Creado grafo de caracteres - TRIGRAMAS")

		if not tri_words_graph.has_edge_definition(TRI_CHAR_EDGE):
			tri_words_graph.create_edge_definition(TRI_CHAR_EDGE, [TRI_CHAR_NODE], [TRI_CHAR_NODE])

# ---------------------------------------------------------- QUERIES DB RELATED FUNCTIONS ----------------------------------------------------------
def find_ngram(db, ngram: str, collection_name: str):
	if collection_name not in GRAPH_TO_COLLECTION.values():
		return None
	
	words_collection = db.collection(collection_name)
	finded_word = None
	cursor = words_collection.find({'name': ngram})
	if not cursor.empty():
		finded_word = cursor.next()

	return finded_word

# Give most likely path between two given words
# origin and goal are _id fields of the respective words
def path_given_two_unigrams(db_aql, origin, goal, graph):
	query = """FOR v, e IN OUTBOUND SHORTEST_PATH '{}' TO '{}' 
        GRAPH '{}' 
        OPTIONS {{
            weightAttribute: 'inverse_count', 
            defaultWeight: 0 
        }}
        RETURN [v._key, v.name, e._key, e.from_name, e.to_name, e.count, e.inverse_count]"""
	
	cursor = db_aql.execute(query.format(origin, goal, graph))
	return [doc for doc in cursor]

def path_end_words(db_aql, origin, graph):
	condition = ""
	if graph == BI_CHARS_GRAPH:
		condition = "second"
	elif graph == TRI_CHARS_GRAPH:
		condition = "third"

	query = """FOR v, e, p IN 1..10 OUTBOUND '{}' GRAPH '{}'
      PRUNE v.{} == '</>'
      OPTIONS {{ weightAttribute: 'inverse_count', defaultWeight: 0, order: 'weighted'}}
      FILTER v.{} == '</>'
      LIMIT 1
      RETURN  {{nodes: p.vertices[*].name, edges: p.edges[*].to_name, inverse_count: p.edges[*].inverse_count}}"""
	
	cursor = db_aql.execute(query.format(origin, graph, condition, condition))
	return cursor.next()

# Give a ordered list of words that usually follow the given word
def recommend_ngram_list(ngram_graph, ngram_hash: str ) -> List[dict]:
	if ngram_graph.name not in GRAPH_TO_OPTION.keys():
		return []

	paths = ngram_graph.traverse(
		start_vertex = GRAPH_TO_COLLECTION[ngram_graph.name] + "/" + ngram_hash,
		direction = "outbound",
		strategy = "bfs",
		min_depth = 1,
		max_depth = 1
	)["paths"] # return lista de palabras conectadas, con longitud maxima de 1
	
	# ordenar los ejes porcampoinverso y sacar la mas frecuentes
	edges = [path["edges"][0] for path in paths]  
	return list(sorted([
		{
			"word_key": edge["_to"].split("/")[1],
			"word_name": edge["to_name"],
			"inverse_count": edge["inverse_count"],
			"count": edge["count"]
		} 
	for edge in edges], key = lambda x: x["inverse_count"]))

# Give a random following word of a discrete distribution sample
def random_word_sample(ngram_graph, ngram_hash: str) -> str:
	if ngram_graph.name not in GRAPH_TO_OPTION.keys():
		return ""
	
	paths = ngram_graph.traverse(
		start_vertex = GRAPH_TO_COLLECTION[ngram_graph.name] + "/" + ngram_hash,
		direction = "outbound",
		strategy = "bfs",
		min_depth = 1,
		max_depth = 1
	)["paths"] # return lista de palabras conectadas, con longitud maxima de 1

	edges = [path["edges"][0] for path in paths]
	if edges:
		total_count = sum(edge["count"] for edge in edges)
		words_to_int = {}
		int_to_words = {}
		int_words = []
		word_chances = []
		i = 0
		for edge in edges:
			words_to_int[edge["to_name"]] = i
			int_to_words[i] = edge["to_name"]
			int_words.append(i)
			word_chances.append(edge["count"] / total_count)
			i += 1
		
		following_words_sample = rv_discrete(name='following_words', values=(int_words, word_chances))
		return int_to_words[following_words_sample.rvs(size=1)[0]]
	
	return ""