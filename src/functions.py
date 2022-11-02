from hashlib import sha256
import itertools
import re #To split string by multiple delimiters
from typing import List
from scipy.stats import rv_discrete
from src.constants import BI_CHAR_EDGE, BI_CHAR_NODE, BI_CHARS_GRAPH, BI_WORD_EDGE, BI_WORD_NODE, BI_WORDS_GRAPH, EDGE_SEPARATOR, TRI_CHAR_EDGE, TRI_CHAR_NODE, TRI_CHARS_GRAPH, TRI_WORD_EDGE, TRI_WORD_NODE, TRI_WORDS_GRAPH, UNI_CHAR_EDGE, UNI_CHAR_NODE, UNI_CHARS_GRAPH, UNI_WORD_EDGE, UNI_WORD_NODE, UNI_WORDS_GRAPH, NODE_SEPARATOR, WORD_FINAL_SYMBOL, WORD_START_SYMBOL

size_to_collection = {1: UNI_WORD_NODE, 2: BI_WORD_NODE, 3: TRI_WORD_NODE}
# ---------------------------------------------------------- DATA READ FUNCTIONS ----------------------------------------------------------
#Read txt files
def read_txt(file_paths: list):
	if type(file_paths) != list:
		raise Exception("The argument specified it is not a list of string")

	#init of empty dicts
	uni_words = {}
	uni_follows = {}
	bi_words = {}
	bi_follows = {}
	tri_words = {}
	tri_follows = {}

	uni_chars = {}
	uni_char_follows = {}
	bi_chars = {}
	bi_char_follows = {}
	tri_chars = {}
	tri_char_follows = {}

	book = 1
	for path in file_paths:
		#open text file
		print("---- Inicio Libro: " + str(book) + " ----")
		file = open(path)
		book_text = file.read()

		uni_reader(book_text, uni_words, uni_follows)
		bi_reader(book_text, bi_words, bi_follows)
		tri_reader(book_text, tri_words, tri_follows)

		#Close text file
		file.close()
		print("---- FIN Libro: " + str(book) + " ----")
	
		book += 1

	return uni_words, uni_follows, bi_words, bi_follows, tri_words, tri_follows

def clean_word(word: str):
	#Delete the only spelling mark left by regex matching and lower the word
	cleaned = (word.lower()).replace("_","")
	#Correct old use of á preposition in books used
	if cleaned == "á":
		cleaned = "a"
	
	return cleaned

# Add start and ending symbol inside a word
def add_boundary_symbols(word: str) -> list:
	word_array = [WORD_START_SYMBOL]
	word_array.extend(list(word))
	word_array.append(WORD_FINAL_SYMBOL)

	return word_array

def uni_char_reader(word: str, uni_chars: dict, uni_char_follows: dict):
	
	last_char = None
	word_array = add_boundary_symbols(word)

	for char in word_array:
		if last_char != None:
			if last_char not in uni_char_follows:
				uni_char_follows[last_char] = {char: 1}
			elif char in uni_char_follows[last_char]:
				uni_char_follows[last_char][char] = uni_char_follows[last_char][char] + 1
			else:
				uni_char_follows[last_char][char] = 1

		if char in uni_chars:
			uni_chars[char] = uni_chars[char] + 1
			
		else:
			uni_chars[char] = 1

		last_char = char

# Read unigrams and theirs relations with other unigrams given a book text.
# uni_words and uni_follows are mutated because they are passed by reference.
def uni_reader(book_text: str, uni_words: dict, uni_follows: dict):
	line_count = 0
	new_unigrams = 0
	known_unigrams = 0
	total_words = 0

	for sentence in book_text.split("."):
		#Give me an array containing each word in that sentence
		array = re.findall(r'\b\w+\b', sentence)
		last_word = None
		for word in array:
			lower_word = clean_word(word)

			if last_word != None:
				if last_word not in uni_follows:
					uni_follows[last_word] = {lower_word: 1}
				elif lower_word in uni_follows[last_word]:
					uni_follows[last_word][lower_word] = uni_follows[last_word][lower_word] + 1
				else:
					uni_follows[last_word][lower_word] = 1

			if lower_word in uni_words:
				uni_words[lower_word] = uni_words[lower_word] + 1
				known_unigrams += 1
				
			else:
				uni_words[lower_word] = 1
				new_unigrams += 1

			last_word = lower_word
			total_words += 1
		
		line_count += 1
		
	print("Analizados nuevos " + str(new_unigrams) + " y conocidos " + str(known_unigrams) + " UNIGRAMAS de " + str(total_words) + " palabras en " + str(line_count) + " sentencias")

# This is an aux function to iterate by bigrams on a string array
def pairwise(array: list):
    a, b = itertools.tee(array)
    next(b, None)
    return zip(a, b)

# Read bigrams and theirs relations with other bigrams given a book text.
# bi_words and bi_follows are mutated because they are passed by reference.
def bi_reader(book_text: str, bi_words: dict, bi_follows: dict):
	line_count = 0
	total_words = 0
	new_bigrams = 0
	known_bigrams = 0

	for sentence in book_text.split("."):
		#Give me an array containing each word in that sentence
		array = re.findall(r'\b\S+\b', sentence)
		last_bigram = None
		for first_word, second_word in pairwise(array):
			bigram = clean_word(first_word) + NODE_SEPARATOR + clean_word(second_word)
			if last_bigram != None:
				if last_bigram not in bi_follows:
					bi_follows[last_bigram] = {bigram: 1}
				elif bigram in bi_follows[last_bigram]:
					bi_follows[last_bigram][bigram] = bi_follows[last_bigram][bigram] + 1
				else:
					bi_follows[last_bigram][bigram] = 1

			if bigram in bi_words:
				bi_words[bigram] = bi_words[bigram] + 1
				known_bigrams += 1

			else:
				bi_words[bigram] = 1
				new_bigrams += 1

			last_bigram = bigram
			total_words += 1
		
		line_count += 1
		
	print("Analizados nuevos " + str(new_bigrams) + " y conocidos " + str(known_bigrams) + " BIGRAMAS de " + str(total_words) + " palabras en " + str(line_count) + " sentencias")

# This is an aux function to iterate by trigrams on a string array
def triwise(array: list):
    a, b,c  = itertools.tee(array, 3)
    next(b, None)
    next(c, None)
    next(c, None)
    return zip(a, b,c)

# Read trigrams and theirs relations with other trigrams given a book text.
# tri_words and tri_follows are mutated because they are passed by reference.
def tri_reader(book_text: str, tri_words: dict, tri_follows: dict):
	line_count = 0
	total_words = 0
	new_trigrams = 0
	known_trigrams = 0

	for sentence in book_text.split("."):
		#Give me an array containing each word in that sentence
		array = re.findall(r'\b\w+\b', sentence)
		last_trigram = None
		for first_word, second_word, third_word in triwise(array):
			trigram = clean_word(first_word) + NODE_SEPARATOR + clean_word(second_word) + NODE_SEPARATOR + clean_word(third_word)
			if last_trigram != None:
				if last_trigram not in tri_follows:
					tri_follows[last_trigram] = {trigram: 1}
				elif trigram in tri_follows[last_trigram]:
					tri_follows[last_trigram][trigram] = tri_follows[last_trigram][trigram] + 1
				else:
					tri_follows[last_trigram][trigram] = 1

			if trigram in tri_words:
				tri_words[trigram] = tri_words[trigram] + 1
				known_trigrams += 1

			else:
				tri_words[trigram] = 1
				new_trigrams += 1

			last_trigram = trigram
			total_words += 1
		
		line_count += 1
		
	print("Analizados nuevos " + str(new_trigrams) + " y conocidos " + str(known_trigrams) + " BIGRAMAS de " + str(total_words) + " palabras en " + str(line_count) + " sentencias")

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
			if(inserted_nodes % 1000 == 0):
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
			if(inserted_nodes % 1000 == 0):
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
def find_ngram(db, ngram: str, size_ngram: int):
	if size_ngram <= 0 or size_ngram > 3:
		return None
	
	words_collection = db.collection(size_to_collection[size_ngram])
	finded_word = None
	cursor = words_collection.find({'name': ngram})
	if not cursor.empty():
		finded_word = cursor.next()

	return finded_word

# Give most likely path between two given words
# origin and goal are _id fields of the respective words
def path_given_two_words(db_aql, origin, goal):
	query = """FOR v, e IN OUTBOUND SHORTEST_PATH '{}' TO '{}' 
        GRAPH 'relatedWords' 
        OPTIONS {{
            weightAttribute: 'inverse_count', 
            defaultWeight: 0 
        }}
        RETURN [v._key, v.name, e._key, e.from_name, e.to_name, e.count, e.inverse_count]"""
	
	cursor = db_aql.execute(query.format(origin, goal))
	return [doc for doc in cursor]

# Give a ordered list of words that usually follow the given word
def recommend_ngram_list(ngram_graph, ngram_hash: str, size_ngram: int) -> List[dict]:
	if size_ngram <= 0 or size_ngram > 3:
		return []

	paths = ngram_graph.traverse(
		start_vertex = size_to_collection[size_ngram] + "/" + ngram_hash,
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
def random_word_sample(ngram_graph, ngram_hash: str, size_ngram: int) -> dict:
	paths = ngram_graph.traverse(
		start_vertex = size_to_collection[size_ngram] + "/" + ngram_hash,
		direction = "outbound",
		strategy = "bfs",
		min_depth = 1,
		max_depth = 1
	)["paths"] # return lista de palabras conectadas, con longitud maxima de 1

	edges = [path["edges"][0] for path in paths]

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

# ---------------------------------------------------------- FEATURE RELATED FUNCTIONS ----------------------------------------------------------
def unigram_recommend_list(db):
	word = input("Introduce una palabra: ")
	max_tam = int(input("Especifica el tamaño máximo de la lista a devolver: "))

	finded = find_ngram(db, word, 1)
	if finded is None:
		print(word + " no se encuentra en el modelo de unigramas")
	
	else:
		uni_graph = db.graph(UNI_WORDS_GRAPH)
		suggestion_list = recommend_ngram_list(uni_graph, finded['_key'], 1)

		return_list = []
		for suggestion in suggestion_list:
			return_list.append((suggestion['word_name'], suggestion['count']))
			if len(return_list) >= max_tam:
				break
		
		print(return_list)

def bigram_recommend_list(db):
	bigram = input("Introduce dos palabras separadas por un espacio: ")
	max_tam = int(input("Especifica el tamaño máximo de la lista a devolver: "))

	finded = find_ngram(db, bigram, 2)
	if finded is None:
		print(bigram + " no se encuentra en el modelo de bigramas")
	
	else:
		bi_graph = db.graph(BI_WORDS_GRAPH)
		suggestion_list = recommend_ngram_list(bi_graph, finded['_key'], 2)

		return_list = []
		for suggestion in suggestion_list:
			return_list.append((suggestion['word_name'], suggestion['count']))
			if len(return_list) >= max_tam:
				break
		
		print(return_list)

def trigram_recommend_list(db):
	trigram = input("Introduce tres palabras separadas por espacios: ")
	max_tam = int(input("Especifica el tamaño máximo de la lista a devolver: "))

	finded = find_ngram(db, trigram, 3)
	if finded is None:
		print(trigram + " no se encuentra en el modelo de trigramas")
	
	else:
		tri_graph = db.graph(TRI_WORDS_GRAPH)
		suggestion_list = recommend_ngram_list(tri_graph, finded['_key'], 3)

		return_list = []
		for suggestion in suggestion_list:
			return_list.append((suggestion['word_name'], suggestion['count']))
			if len(return_list) >= max_tam:
				break
		
		print(return_list)

def unigram_suggestion(db):
	word = input("Introduce una palabra: ")
	finded = find_ngram(db, word, 1)
	if finded is None:
		print(word + " no se encuentra en el modelo de unigramas")

	else:
		uni_graph = db.graph(UNI_WORDS_GRAPH)
		suggestion = random_word_sample(uni_graph, finded['_key'],1)
		print("Te sugiero ante " + word + " la palabra " + suggestion)

def bigram_suggestion(db):
	bigram = input("Introduce dos palabras separadas por un espacio: ")
	finded = find_ngram(db, bigram, 2)
	if finded is None:
		print(bigram + " no se encuentra en el modelo de bigramas")

	else:
		bi_graph = db.graph(BI_WORDS_GRAPH)
		suggestion = random_word_sample(bi_graph, finded['_key'], 2)
		print("Te sugiero ante el bigrama: '" + bigram + "' la palabra: '" + suggestion.split(" ")[1] + "' porque el siguiente bigrama sugerido es: '" + suggestion + "'")

def trigram_suggestion(db):
	trigram = input("Introduce tres palabras separadas por un espacio: ")
	finded = find_ngram(db, trigram, 3)
	if finded is None:
		print(trigram + " no se encuentra en el modelo de trigramas")

	else:
		tri_graph = db.graph(TRI_WORDS_GRAPH)
		suggestion = random_word_sample(tri_graph, finded['_key'], 3)
		print("Te sugiero ante el trigrama: '" + trigram + "' la palabra: '" + suggestion.split(" ")[2] + "' porque el siguiente trigrama sugerido es: '" + suggestion + "'")

#Aux function to most_likey_path functions
def give_new_first_ngram(list, used_ngrams):
	for possible_ngram in list:
		if possible_ngram['word_name'] not in used_ngrams:
			return possible_ngram

	return None

def unigram_most_likey_path(db):
	word = input("Introduce una palabra que inicie la frase: ")
	max_tam = int(input("Especifica el tamaño máximo de la frase que quieres formar: "))

	finded = find_ngram(db, word, 1)
	if finded is None:
		print(word + " no se encuentra en el modelo de unigramas")
	
	else:
		used_words = [word]
		uni_graph = db.graph(UNI_WORDS_GRAPH)
		for i in range(max_tam - 1):
			list = recommend_ngram_list(uni_graph, finded['_key'], 1)
			next_word = give_new_first_ngram(list, used_words)
			if next_word is None:
				break
			word = word + " " + next_word['word_name']
			used_words.append(next_word['word_name'])
			finded = find_ngram(db, next_word['word_name'], 1)

		print(word)

def bigram_most_likely_path(db):
	bigram = input("Introduce dos palabras separadas por un espacio: ")
	max_tam = int(input("Especifica el tamaño máximo de la frase que quieres formar: "))

	finded = find_ngram(db, bigram, 2)
	if finded is None:
		print(bigram + " no se encuentra en el modelo de bigramas")
	
	else:
		bi_graph = db.graph(BI_WORDS_GRAPH)
		used_bigram = [bigram]
		for i in range(max_tam - 2):
			list = recommend_ngram_list(bi_graph, finded['_key'], 2)
			next_word = give_new_first_ngram(list, used_bigram)
			if next_word is None:
				break
			bigram = bigram + " " + next_word['word_name'].split(" ")[1]
			used_bigram.append(next_word['word_name'])
			finded = find_ngram(db, next_word['word_name'], 2)

		print(bigram)

def trigram_most_likely_path(db):
	trigram = input("Introduce tres palabras separadas por un espacio: ")
	max_tam = int(input("Especifica el tamaño máximo de la frase que quieres formar: "))

	finded = find_ngram(db, trigram, 3)
	if finded is None:
		print(trigram + " no se encuentra en el modelo de trigramas")
	
	else:
		tri_graph = db.graph(TRI_WORDS_GRAPH)
		used_trigram = [trigram]
		for i in range(max_tam - 3):
			list = recommend_ngram_list(tri_graph, finded['_key'], 3)
			next_word = give_new_first_ngram(list, used_trigram)
			if next_word is None:
				break
			trigram = trigram + " " + next_word['word_name'].split(" ")[2]
			used_trigram.append(next_word['word_name'])
			finded = find_ngram(db, next_word['word_name'], 3)

		print(trigram)




def unigram_path_two_words(db):
	print("Dame dos palabras y te dire el camino más probable entre las dos: ")
	word1 = input("Primera: ")
	origin = find_ngram(db, word1, 1)
	word2 = input("Segunda: ")
	goal = find_ngram(db, word2, 1)
	if origin is None:
		print(word1 + " no se encuentra en el modelo de unigramas")

	elif goal is None:
		print(word2 + " no se encuentra en el modelo de unigramas")

	else:
		path = path_given_two_words(db.aql, origin['_id'], goal['_id'])
		phrase = ''
		for doc in path:
			phrase = phrase + " " + doc[1]
		print(phrase)

def phrase_suggestions(db, phrase = None):
	suggestions_dict = {
		"unigram": "",
		"bigram": "",
		"trigram": ""
	}
	
	if phrase is None:
		phrase = input("Frase: ")

	word_array = re.findall(r'\b\w+\b', phrase)
	phrase_len = len(word_array)

	if phrase_len >= 1:
		finded = find_ngram(db, word_array[-1], 1)
		if finded is not None:
			list = recommend_ngram_list(db.graph(UNI_WORDS_GRAPH), finded['_key'], 1)
			if list:
				suggestions_dict["unigram"] = list[0]['word_name']

	if phrase_len >= 2:
		finded = find_ngram(db, word_array[-2] + ' ' + word_array[-1], 2)
		if finded is not None:
			list = recommend_ngram_list(db.graph(BI_WORDS_GRAPH), finded['_key'], 2)
			if list:
				suggestions_dict["bigram"] = list[0]['word_name'].split(' ')[-1]

	if phrase_len >= 3:
		finded = find_ngram(db, word_array[-3] + ' ' + word_array[-2] + ' ' + word_array[-1], 3)
		if finded is not None:
			list = recommend_ngram_list(db.graph(TRI_WORDS_GRAPH), finded['_key'], 3)
			if list:
				suggestions_dict["trigram"] = list[0]['word_name'].split(' ')[-1]

	return suggestions_dict

# ---------------------------------------------------------- MENU RELATED FUNCTIONS ----------------------------------------------------------
def option_display(options: list) -> int:
	count = 1
	for option in options:
		print(str(count) + " - " + option)
		count += 1
	
	return int(input('Indique el modo: '))

def main_menu(db):
	print("Bienvenido a GPG, porfavor selecciona con que n-gramas quieres trabajar: ")
	chosen = option_display(["Funcionalidades con Unigramas", "Funcionalidades con Bigramas", "Funcionalidades con Trigramas", "Salir"])
	match chosen:
		case 1:
			unigram_menu(db)
		case 2:
			bigram_menu(db)
		case 3:
			trigram_menu(db)
		case 4:
			exit()
		case _:
			print("Entrada no reconocida. Introduzca un valor del 1-4")

def unigram_menu(db):
	print("---- Elige una de las funcionalidades disponibles con UNIGRAMAS ----")
	chosen = option_display(["Lista por probabilidades de aparición","Sugiere una palabra","Camino más probable entre dos palabras", "Camino más probable dado tamaño maximo", "Volver atrás", "Salir"])
	match chosen:
		case 1:
			unigram_recommend_list(db)
		case 2:
			unigram_suggestion(db)
		case 3:
			unigram_path_two_words(db)
		case 4:
			unigram_most_likey_path(db)
		case 5:
			""
		case 6:
			exit()
		case _:
			print("Entrada no reconocida de entres las posibles volviendo al menu principal...")
	
	main_menu(db)
			

def bigram_menu(db):
	print("---- Elige una de las funcionalidades disponibles con BIGRAMAS ----")
	chosen = option_display(["Lista por probabilidades de aparición","Sugiere una palabra dado un bigrama","Camino más probable dado tamaño maximo", "Volver atrás", "Salir"])
	match chosen:
		case 1:
			bigram_recommend_list(db)
		case 2:
			bigram_suggestion(db)
		case 3:
			bigram_most_likely_path(db)
		case 4:
			""
		case 5:
			exit()
		case _:
			print("Entrada no reconocida de entres las posibles volviendo al menu principal...")

	main_menu(db)

def trigram_menu(db):
	print("---- Elige una de las funcionalidades disponibles con TRIGRAMAS ----")
	chosen = option_display(["Lista por probabilidades de aparición","Sugiere una palabra dado un trigrama", "Camino más probable dado tamaño maximo", "Volver atrás", "Salir"])
	match chosen:
		case 1:
			trigram_recommend_list(db)
		case 2:
			trigram_suggestion(db)
		case 3:
			trigram_most_likely_path(db)
		case 4:
			""
		case 5:
			exit()
		case _:
			print("Entrada no reconocida de entres las posibles volviendo al menu principal...")
	
	main_menu(db)