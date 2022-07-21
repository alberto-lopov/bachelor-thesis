import re #To split string by multiple delimiters

#Read txt files
def readTxt(pathFile: str):
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