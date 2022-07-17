#Read txt files
import re #To split string by multiple delimiters

#init of an empty dict
wordMap = {}

#open text file
file = open("./books/prueba.txt")

for line in file:
	#debug: print(re.findall(r'\b\S+\b', line))
	array = re.findall(r'\b\S+\b', line)
	for word in array:
		if(wordMap.get(word) == None):
			wordMap[word] = 1
		else:
			wordMap[word] = wordMap[word] + 1 

print(wordMap)

file.close()