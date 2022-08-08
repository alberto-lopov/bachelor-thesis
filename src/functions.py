import re #To split string by multiple delimiters
from typing import List

from src.constants import NODE_COLLECTION

#Read txt files
def read_txt(pathFile: str):
	if type(pathFile) != str:
		raise Exception("The argument specified it is not a string")

	#init of an empty dict
	wordMap = {}
	followingWords = {}

	#open text file
	file = open(pathFile)

	for line in file:
		#Give me an array containing each word in that line
		array = re.findall(r'\b\S+\b', line)
		lastWord = None
		for word in array:
			if lastWord != None:
				if lastWord not in followingWords:
					followingWords[lastWord] = {word: 1}
				elif word in followingWords[lastWord]:
					followingWords[lastWord][word] = followingWords[lastWord][word] + 1
				else:
					followingWords[lastWord][word] = 1

			if word in wordMap:
				wordMap[word] = wordMap[word] + 1
				
			else:
				wordMap[word] = 1

			lastWord = word

	file.close()
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