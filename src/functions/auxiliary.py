import itertools

from src.constants import WORD_FINAL_SYMBOL, WORD_START_SYMBOL

def clean_word(word: str):
	# Delete the only spelling mark left by regex matching and lower the word
	cleaned = (word.lower()).replace("_","")
	
	# Correct old use of á, ó, ú preposition on used spanish books 
	if cleaned == "á":
		cleaned = "a"
	elif cleaned == "ó":
		cleaned = "o"
	elif cleaned == "ú":
		cleaned = "u"
	
	return cleaned

# Add start and ending symbol inside a word
def add_boundary_symbols(word: str) -> list:
	word_array = [WORD_START_SYMBOL]
	word_array.extend(list(word))
	word_array.append(WORD_FINAL_SYMBOL)

	return word_array

# This is an aux function to iterate by bigrams on a string array
def pairwise(array: list):
    a, b = itertools.tee(array)
    next(b, None)
    return zip(a, b)

# This is an aux function to iterate by trigrams on a string array
def triwise(array: list):
    a, b,c  = itertools.tee(array, 3)
    next(b, None)
    next(c, None)
    next(c, None)
    return zip(a, b,c)