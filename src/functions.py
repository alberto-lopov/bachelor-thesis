import re #To split string by multiple delimiters
from typing import List
from scipy.stats import rv_discrete
from src.constants import NODE_COLLECTION

#Read txt files
def read_txt(file_paths: list):
	if type(file_paths) != list:
		raise Exception("The argument specified it is not a list of string")

	#init of an empty dict
	wordMap = {}
	followingWords = {}

	book = 1
	for path in file_paths:
		#open text file
		print("---- Inicio Libro: " + str(book) + " ----")
		file = open(path)

		line_count = 0
		for line in file:
			#Give me an array containing each word in that line
			array = re.findall(r'\b\S+\b', line)
			lastWord = None
			for word in array:
				lower_word = word.lower()
				if lastWord != None:
					if lastWord not in followingWords:
						followingWords[lastWord] = {lower_word: 1}
					elif lower_word in followingWords[lastWord]:
						followingWords[lastWord][lower_word] = followingWords[lastWord][lower_word] + 1
					else:
						followingWords[lastWord][lower_word] = 1

				if lower_word in wordMap:
					wordMap[lower_word] = wordMap[lower_word] + 1
					
				else:
					wordMap[lower_word] = 1

				lastWord = lower_word
			
			line_count += 1
		print("Analizada lineas: " + str(line_count) + " de libro: " + str(book))

		file.close()
		print("---- Fin Libro: " + str(book) + " ----")
		book += 1

	return wordMap, followingWords

def find_word(db_aql, word: str):
	query = """FOR word IN words 
		FILTER word.name == '{}' 
		RETURN word
	"""

	cursor = db_aql.execute(query.format(word))
	return cursor.next()

# Give most likely path between two given words
# origin and goal are _id fields of the respective words
def most_likely_path(db_aql, origin, goal):
	query = """FOR v, e IN OUTBOUND SHORTEST_PATH '{}' TO '{}' 
        GRAPH 'relatedWords' 
        OPTIONS {{
            weightAttribute: 'count', 
            defaultWeight: 0 
        }}
        RETURN [v._key, v.name, e._key, e.from_name, e.to_name, e.count, e.inverse_count]"""
	
	cursor = db_aql.execute(query.format(origin, goal))
	return [doc for doc in cursor]



# Give a ordered list of words that usually follow the given word
def recommend(words_graph, word_hash: str) -> List[dict]:
	paths = words_graph.traverse(
		start_vertex = NODE_COLLECTION + "/" + word_hash,
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
		start_vertex = NODE_COLLECTION + "/" + word_hash,
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
