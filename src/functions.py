import re #To split string by multiple delimiters

#Read txt files
def readTxt(pathFile: str):
	if type(pathFile) != str:
		raise Exception("The argument specified it is not a string")

	#init of an empty dict
	wordMap = {}

	#open text file
	file = open(pathFile)

	for line in file:
		#Give me an array containing each word in that line
		array = re.findall(r'\b\S+\b', line)
		for word in array:
			if word in wordMap:
				wordMap[word] = wordMap[word] + 1
				
			else:
				wordMap[word] = 1

	file.close()
	return wordMap