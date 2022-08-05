import re #To split string by multiple delimiters

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
        RETURN [v._key, v.name, e._key, e.count, e.inverse_count]"""

	cursor = db_aql.execute(query.format(origin, goal))
	return [doc for doc in cursor]

"""EJEMPLO DE QUERY FUNCIONAL:
FOR v, e IN OUTBOUND SHORTEST_PATH 'words/1b7f8466f087c27f24e1c90017b829cd8208969018a0bbe7d9c452fa224bc6cc' TO 'words/8e317f8df6bcc28e25cc1bf9aa449d68679ce17b53a0cb2b2cfce188031380dc' 
        GRAPH 'relatedWords' 
        OPTIONS {
            weightAttribute: 'count',
            defaultWeight: 0
        }
        RETURN [v._key, v.name, e._key, e.count, e.inverse_count]"""