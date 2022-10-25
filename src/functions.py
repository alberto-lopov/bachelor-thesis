from hashlib import sha256
import itertools
import re #To split string by multiple delimiters
from typing import List
from scipy.stats import rv_discrete
from src.constants import BI_EDGE_COLLECTION, BI_NODE_COLLECTION, BI_WORDS_GRAPH, EDGE_SEPARATOR, TRI_EDGE_COLLECTION, TRI_NODE_COLLECTION, TRI_WORDS_GRAPH, UNI_EDGE_COLLECTION, UNI_NODE_COLLECTION, UNI_WORDS_GRAPH, WORD_SEPARATOR

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

# Read unigrams and theirs relations with other unigrams given a book text.
# uni_words and uni_follows are mutated because they are passed by reference.
def uni_reader(book_text: str, uni_words: dict, uni_follows: dict):
	line_count = 0
	new_unigrams = 0
	known_unigrams = 0
	total_words = 0

	for sentence in book_text.split("."):
		#Give me an array containing each word in that sentence
		array = re.findall(r'\b\S+\b', sentence)
		last_word = None
		for word in array:
			lower_word = word.lower()
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
			bigram = (first_word + WORD_SEPARATOR + second_word).lower()
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
			trigram = (first_word + WORD_SEPARATOR + second_word + WORD_SEPARATOR + third_word).lower()
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

def unigram_initialization(db, uni_words, uni_follows):
	
	# Add nodes
	if not db.has_collection(UNI_NODE_COLLECTION):
		words = db.create_collection(UNI_NODE_COLLECTION)
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
				print("Insertados " + str(inserted_nodes) + " nodos de UNIGRAMAS")

	# Add edges
	if not db.has_collection(UNI_EDGE_COLLECTION):
		follows = db.create_collection(UNI_EDGE_COLLECTION, edge=True)
		
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
				print("Insertados " + str(inserted_edges) + " arcos de UNIGRAMAS")

	# --- Create graphs
	if not db.has_graph(UNI_WORDS_GRAPH):
		related_words_graph = db.create_graph(UNI_WORDS_GRAPH)
		print("Creado grafo de UNIGRAMAS")

		if not related_words_graph.has_edge_definition(UNI_EDGE_COLLECTION):
			related_words_graph.create_edge_definition(UNI_EDGE_COLLECTION, [UNI_NODE_COLLECTION], [UNI_NODE_COLLECTION])

def bigram_initialization(db, bi_words, bi_follows):
	
	# Add nodes
	if not db.has_collection(BI_NODE_COLLECTION):
		bi_node = db.create_collection(BI_NODE_COLLECTION)
		bi_node.add_fulltext_index(fields=["name"])

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
			if(inserted_nodes % 1000 == 0):
				print("Insertados " + str(inserted_nodes) + " nodos de BIGRAMAS")

	# Add edges
	if not db.has_collection(BI_EDGE_COLLECTION):
		bi_edge = db.create_collection(BI_EDGE_COLLECTION, edge=True)
		
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
				print("Insertados " + str(inserted_edges) + " arcos de BIGRAMAS")

	if not db.has_graph(BI_WORDS_GRAPH):
		bi_words_graph = db.create_graph(BI_WORDS_GRAPH)
		print("Creado grafo de BIGRAMAS.")

		if not bi_words_graph.has_edge_definition(BI_EDGE_COLLECTION):
			bi_words_graph.create_edge_definition(BI_EDGE_COLLECTION, [BI_NODE_COLLECTION], [BI_NODE_COLLECTION])

def trigram_initialization(db, tri_words, tri_follows):
	
	# Add nodes
	if not db.has_collection(TRI_NODE_COLLECTION):
		tri_node = db.create_collection(TRI_NODE_COLLECTION)
		tri_node.add_fulltext_index(fields=["name"])

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
			if(inserted_nodes % 1000 == 0):
				print("Insertados " + str(inserted_nodes) + " nodos de TRIGRAMAS")

	# Add edges
	if not db.has_collection(TRI_EDGE_COLLECTION):
		tri_edge = db.create_collection(TRI_EDGE_COLLECTION, edge=True)
		inserted_edges = 0
		for key, value in tri_follows.items():
			for key2, value2 in value.items():
				tri_edge.insert({
					"_key": sha256((key + EDGE_SEPARATOR + key2).encode()).hexdigest(),
					"_from": TRI_NODE_COLLECTION + '/' + sha256(key.encode()).hexdigest(),
					"_to": TRI_NODE_COLLECTION + '/' + sha256(key2.encode()).hexdigest(),
					"count": value2,
					"from_name": key.replace(WORD_SEPARATOR, " "),
					"to_name": key2.replace(WORD_SEPARATOR, " "),
					"inverse_count": 1/value2
				})
			inserted_edges += 1
			if(inserted_edges % 10 == 0):
				print("Insertados " + str(inserted_edges) + " arcos de TRIGRAMAS")

	if not db.has_graph(TRI_WORDS_GRAPH):
		tri_words_graph = db.create_graph(TRI_WORDS_GRAPH)
		print("Creado grafo de TRIGRAMAS")

		if not tri_words_graph.has_edge_definition(TRI_EDGE_COLLECTION):
			tri_words_graph.create_edge_definition(TRI_EDGE_COLLECTION, [TRI_NODE_COLLECTION], [TRI_NODE_COLLECTION])

# ---------------------------------------------------------- QUERIES DB RELATED FUNCTIONS ----------------------------------------------------------
def find_word(db, word: str):
	words_collection = db.collection(UNI_NODE_COLLECTION)
	finded_word = None
	cursor = words_collection.find({'name': word})
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
def recommend(words_graph, word_hash: str) -> List[dict]:
	paths = words_graph.traverse(
		start_vertex = UNI_NODE_COLLECTION + "/" + word_hash,
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
def random_word_sample(words_graph, word_hash: str) -> dict:
	paths = words_graph.traverse(
		start_vertex = UNI_NODE_COLLECTION + "/" + word_hash,
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
def unigram_recommend(db):
	word = input("Introduce una palabra: ")
	max_tam = int(input("Especifica el tamaño máximo de la lista a devolver: "))

	finded = find_word(db, word)
	if finded is None:
		print(word + " no se encuentra en el modelo")
	
	else:
		uni_graph = db.graph(UNI_WORDS_GRAPH)
		suggestion_list = recommend(uni_graph, finded['_key'])

		return_list = []
		for suggestion in suggestion_list:
			return_list.append((suggestion['word_name'], suggestion['count']))
			if len(return_list) >= max_tam:
				break
		
		print(return_list)

def unigram_suggestion(db):
	word = input("Introduce una palabra: ")
	finded = find_word(db, word)
	if finded is None:
		print(word + " no se encuentra en el modelo")

	else:
		uni_graph = db.graph(UNI_WORDS_GRAPH)
		suggestion = random_word_sample(uni_graph, finded['_key'])
		print("Te sugiero ante " + word + " la palabra " + suggestion)

def unigram_most_likey_path(db):
	word = input("Introduce una palabra que inicie la frase: ")
	max_tam = int(input("Especifica el tamaño máximo de la frase a devolver: "))

	finded = find_word(db, word)
	if finded is None:
		print(word + " no se encuentra en el modelo")
	
	else:
		uni_graph = db.graph(UNI_WORDS_GRAPH)
		for i in range(max_tam - 1):
			next_word = recommend(uni_graph, finded['_key']).pop(1)
			word = word + " " + next_word['word_name']
			finded = find_word(db, next_word['word_name'])

		print(word)

def unigram_path_two_words(db):
	print("Dame dos palabras y te dire el camino más probable entre las dos: ")
	word1 = input("Primera: ")
	origin = find_word(db, word1)
	word2 = input("Segunda: ")
	goal = find_word(db, word2)
	if origin is None:
		print(word1 + " no se encuentra en el modelo")

	elif goal is None:
		print(word2 + " no se encuentra en el modelo")

	else:
		path = path_given_two_words(db.aql, origin['_id'], goal['_id'])
		phrase = ''
		for doc in path:
			phrase = phrase + " " + doc[1]
		print(phrase)


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
			unigram_recommend(db)
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
			

def bigram_menu():
	""

def trigram_menu():
	""