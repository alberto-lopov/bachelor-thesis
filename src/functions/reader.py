import re #To split string by multiple delimiters

from src.constants import NODE_SEPARATOR 
from src.functions.auxiliary import add_boundary_symbols, pairwise, triwise, clean_word

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

		uni_reader(book_text, uni_words, uni_follows, uni_chars, uni_char_follows, bi_chars, bi_char_follows, tri_chars, tri_char_follows)
		bi_reader(book_text, bi_words, bi_follows)
		tri_reader(book_text, tri_words, tri_follows)

		#Close text file
		file.close()
		print("---- FIN Libro: " + str(book) + " ----")
	
		book += 1

	return uni_words, uni_follows, bi_words, bi_follows, tri_words, tri_follows, uni_chars, uni_char_follows, bi_chars, bi_char_follows, tri_chars, tri_char_follows

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

def bi_char_reader(word: str, bi_chars: dict, bi_char_follows: dict):
	
	last_bigram = None
	word_array = add_boundary_symbols(word)

	for first_char, second_char in pairwise(word_array):
		bigram = first_char + NODE_SEPARATOR + second_char
		if last_bigram != None:
			if last_bigram not in bi_char_follows:
				bi_char_follows[last_bigram] = {bigram: 1}
			elif bigram in bi_char_follows[last_bigram]:
				bi_char_follows[last_bigram][bigram] = bi_char_follows[last_bigram][bigram] + 1
			else:
				bi_char_follows[last_bigram][bigram] = 1

		if bigram in bi_chars:
			bi_chars[bigram] = bi_chars[bigram] + 1
			
		else:
			bi_chars[bigram] = 1

		last_bigram = bigram

def tri_char_reader(word: str, tri_chars: dict, tri_char_follows: dict):
	
	last_trigram = None
	word_array = add_boundary_symbols(word)

	for first_char, second_char, third_char in triwise(word_array):
		trigram = first_char + NODE_SEPARATOR + second_char + NODE_SEPARATOR + third_char
		if last_trigram != None:
			if last_trigram not in tri_char_follows:
				tri_char_follows[last_trigram] = {trigram: 1}
			elif trigram in tri_char_follows[last_trigram]:
				tri_char_follows[last_trigram][trigram] = tri_char_follows[last_trigram][trigram] + 1
			else:
				tri_char_follows[last_trigram][trigram] = 1

		if trigram in tri_chars:
			tri_chars[trigram] = tri_chars[trigram] + 1
			
		else:
			tri_chars[trigram] = 1

		last_trigram = trigram

# Read unigrams and theirs relations with other unigrams given a book text.
# uni_words and uni_follows are mutated because they are passed by reference.
def uni_reader(book_text: str, uni_words: dict, uni_follows: dict, uni_chars: dict, uni_char_follows: dict, bi_chars: dict, bi_char_follows: dict, tri_chars: dict, tri_char_follows: dict):
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
			uni_char_reader(lower_word, uni_chars, uni_char_follows)
			bi_char_reader(lower_word, bi_chars, bi_char_follows)
			tri_char_reader(lower_word, tri_chars, tri_char_follows)

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