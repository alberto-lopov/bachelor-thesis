
import re
from src.constants import BI_CHAR_NODE, BI_CHARS_GRAPH, BI_WORD_NODE, BI_WORDS_GRAPH, GRAPH_TO_COLLECTION, GRAPH_TO_OPTION, TRI_CHAR_NODE, TRI_CHARS_GRAPH, TRI_WORD_NODE, TRI_WORDS_GRAPH, UNI_CHAR_NODE, UNI_CHARS_GRAPH, UNI_WORD_NODE, UNI_WORDS_GRAPH, WORD_FINAL_SYMBOL, WORD_START_SYMBOL
from src.functions.database_interaction import find_ngram, path_end_words, path_given_two_unigrams, random_word_sample, recommend_ngram_list


def display_recommend_list(db, str_graph: str, ask_input: str):
	ngram = input(ask_input).strip()
	max_tam = int(input("Especifica el tamaño máximo de la lista a devolver: "))

	finded = find_ngram(db, ngram, GRAPH_TO_COLLECTION[str_graph])
	if finded is None:
		print(ngram + " no se encuentra en el modelo de " + str_graph)

	else:
		graph = db.graph(str_graph)
		suggestion_list = recommend_ngram_list(graph, finded['_key'])

		return_list = []
		for suggestion in suggestion_list:
			return_list.append([suggestion['word_name'], suggestion['count']])
			if(len(return_list) >= max_tam):
				break

		print(return_list)

def display_sample_suggestion(db, str_graph:str, ask_input: str):
	ngram = input(ask_input).strip()

	finded = find_ngram(db, ngram, GRAPH_TO_COLLECTION[str_graph])
	if finded is None:
		print(ngram + " no se encuentra en el modelo de " + str_graph)

	else:
		graph = db.graph(str_graph)
		suggestion = random_word_sample(graph, finded['_key'])
		# If we are suggesting to char input
		if str_graph in [UNI_CHARS_GRAPH, BI_CHARS_GRAPH, TRI_CHARS_GRAPH]:
			if suggestion.find(WORD_FINAL_SYMBOL) == -1:
				print("Ante el n-grama introducido: '" + ngram + "', mi sugerencia es: '" + suggestion[-1] + "' porque el siguiente ngrama sugerido es: '" + suggestion + "'")
			else:
				print("Ante el n-grama introducido: '" + ngram + "', mi sugerencia es que termines la palabra porque el siguiente ngrama sugerido es: '" + suggestion + "'")
		#If we suggest to word input
		else:
			print("Ante el n-grama introducido: '" + ngram + "', mi sugerencia es: '" + suggestion.split(" ")[-1] + "' porque el siguiente ngrama sugerido es: '" + suggestion + "'")

#Aux function to most_likey_path functions
def give_new_first_ngram(list, used_ngrams):
	for possible_ngram in list:
		if possible_ngram['word_name'] not in used_ngrams:
			return possible_ngram

	return None

def display_most_likely_phrase(db, str_graph: str, ask_input: str):
	ngram = input(ask_input).strip()
	max_tam = int(input("Especifica el tamaño máximo de la frase que quieres formar: "))

	finded = find_ngram(db, ngram, GRAPH_TO_COLLECTION[str_graph])
	if finded is None:
		print("'" + ngram + "' no se encuentra en el modelo de " + str_graph)

	else:
		used_ngrams = [ngram]
		graph = db.graph(str_graph)
		for i in range (max_tam - GRAPH_TO_OPTION[str_graph]):
			list = recommend_ngram_list(graph, finded['_key'])
			next_ngram = give_new_first_ngram(list, used_ngrams)
			if next_ngram is None:
				break
			ngram = ngram + " " + next_ngram['word_name'].split(" ")[-1]
			used_ngrams.append(next_ngram['word_name'])
			finded = find_ngram(db, next_ngram['word_name'], GRAPH_TO_COLLECTION[str_graph])
		
		print(ngram)

def display_autocomplete_word(db, str_graph: str, ask_input: str):
	ngram = input(ask_input)

	suggestion = autocomplete(db, ngram, GRAPH_TO_OPTION[str_graph]-3)
	if suggestion == "":
		print("Ante la palabra: '" + ngram + "', No se sugiere añadir nada más.")
	else:
		print("Para completar la palabra: '"+ ngram + "', Se te sugiere: '" + suggestion + "'")

def unigram_path_two_words(db):
	print("Dame dos palabras y te dire el camino más probable entre las dos: ")
	word1 = input("Primera: ")
	origin = find_ngram(db, word1, UNI_WORD_NODE)
	word2 = input("Segunda: ")
	goal = find_ngram(db, word2, UNI_WORD_NODE)
	if origin is None:
		print(word1 + " no se encuentra en el modelo de unigramas")

	elif goal is None:
		print(word2 + " no se encuentra en el modelo de unigramas")

	else:
		path = path_given_two_unigrams(db.aql, origin['_id'], goal['_id'], UNI_WORDS_GRAPH)
		phrase = ''
		for doc in path:
			phrase = phrase + " " + doc[1]
		print(phrase)

def autocomplete(db, uncompleted_word: str, size_ngram: int):
	suggestion = ""
	stripped_word = []
	if(len(uncompleted_word) < size_ngram):
		stripped_word.append(WORD_START_SYMBOL)

	stripped_word.extend(uncompleted_word.strip())
	size_word = len(stripped_word)

	if size_ngram == 1 and size_word >= 1:
		end_word = find_ngram(db, WORD_FINAL_SYMBOL, UNI_CHAR_NODE)
		finded = find_ngram(db, ''.join(stripped_word[-1]), UNI_CHAR_NODE)
		if finded != None:
			suggestion += uncompleted_word + '-'
			path = path_given_two_unigrams(db.aql, finded['_id'], end_word['_id'], UNI_CHARS_GRAPH)
			for doc in path[1:]:
				suggestion += doc[1]
	
	elif size_ngram == 2 and size_word >= 2:
		finded = find_ngram(db, ''.join(stripped_word[-2:]), BI_CHAR_NODE)
		if finded != None:
			suggestion += uncompleted_word + '-'
			path = path_end_words(db.aql, finded['_id'], BI_CHARS_GRAPH)
			for char in path['edges']:
				suggestion += char[-1]

	elif size_ngram == 3 and size_word >= 3:
		finded = find_ngram(db, ''.join(stripped_word[-3:]), TRI_CHAR_NODE)
		if finded != None:
			suggestion += uncompleted_word + '-'
			path = path_end_words(db.aql, finded['_id'], TRI_CHARS_GRAPH)
			for char in path['edges']:
				suggestion += char[-1]

	clean_suggestion = suggestion.strip('</>')
	# Return suggestion if last character is not "-" and we have that word on our dictionary
	return clean_suggestion if clean_suggestion != "" and clean_suggestion[-1] != '-' and find_ngram(db, clean_suggestion.replace('-',''), UNI_WORD_NODE) != None else ""
	
def next_word_suggestion(db, phrase = None):
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
		finded = find_ngram(db, word_array[-1], UNI_WORD_NODE)
		if finded is not None:
			suggestion = random_word_sample(db.graph(UNI_WORDS_GRAPH), finded['_key'])
			if suggestion:
				suggestions_dict["unigram"] = suggestion.split(" ")[-1]

	if phrase_len >= 2:
		finded = find_ngram(db, word_array[-2] + ' ' + word_array[-1], BI_WORD_NODE)
		if finded is not None:
			suggestion = random_word_sample(db.graph(BI_WORDS_GRAPH), finded['_key'])
			if suggestion:
				suggestions_dict["bigram"] = suggestion.split(" ")[-1]

	if phrase_len >= 3:
		finded = find_ngram(db, word_array[-3] + ' ' + word_array[-2] + ' ' + word_array[-1], TRI_WORD_NODE)
		if finded is not None:
			suggestion = random_word_sample(db.graph(TRI_WORDS_GRAPH), finded['_key'])
			if suggestion:
				suggestions_dict["trigram"] = suggestion.split(" ")[-1]

	return suggestions_dict

def autoword_suggestions(db, phrase = None):
	suggestions_dict = {
		"unigram": "",
		"bigram": "",
		"trigram": ""
	}
	
	if phrase is None:
		phrase = input("Palabra: ")

	word_array = re.findall(r'\b\w+\b', phrase)
	last_word = word_array[-1]

	word_len = len(last_word)
	if word_len >= 1:
		suggestions_dict["unigram"] = autocomplete(db, last_word, 1)
		suggestions_dict["bigram"] = autocomplete(db, last_word, 2)
		
	if word_len >= 2:
		suggestions_dict["trigram"] = autocomplete(db, last_word, 3)

	return suggestions_dict

# ---------------------------------------------------------- MENU RELATED FUNCTIONS ----------------------------------------------------------
def option_display(options: list) -> int:
	count = 1
	for option in options:
		print(str(count) + " - " + option)
		count += 1
	
	return int(input('Indique el modo: '))

def main_menu(db):
	print("Bienvenido a GPG, porfavor selecciona con que modelo de n-gramas quieres trabajar: ")
	chosen = option_display(["Modelos de Caracteres", "Modelos de Palabras", "Salir"])
	match chosen:
		case 1:
			main_char_menu(db)
		case 2:
			main_word_menu(db)
		case 3:
			exit()
		case _:
			print("Entrada no reconocida. Introduzca un valor del 1-3")

def main_char_menu(db):
	print("Caracteres -- Porfavor selecciona con que n-gramas quieres trabajar: ")
	chosen = option_display(["Funcionalidades con Unigramas", "Funcionalidades con Bigramas", "Funcionalidades con Trigramas", "Volver atrás", "Salir"])
	match chosen:
		case 1:
			uni_char_menu(db)
		case 2:
			bi_char_menu(db)
		case 3:
			tri_char_menu(db)
		case 4:
			""
		case 5:
			exit()
		case _:
			print("Entrada no reconocida. Volviendo a menú principal...")
	
	main_menu(db)

def main_word_menu(db):
	print("Palabras -- Porfavor selecciona con que n-gramas quieres trabajar: ")
	chosen = option_display(["Funcionalidades con Unigramas", "Funcionalidades con Bigramas", "Funcionalidades con Trigramas", "Volver atrás", "Salir"])
	match chosen:
		case 1:
			uni_word_menu(db)
		case 2:
			bi_word_menu(db)
		case 3:
			tri_word_menu(db)
		case 4:
			""
		case 5:
			exit()
		case _:
			print("Entrada no reconocida. Volviendo a menú principal...")

	main_menu(db)

def uni_char_menu(db):
	print("---- Caracteres -- Elige una de las funcionalidades disponibles con UNIGRAMAS ----")
	chosen = option_display(["Lista ordenada según probabilidad","Sugiere siguiente caracter","Autocompleta la palabra","Volver atrás", "Salir"])
	match chosen:
		case 1:
			display_recommend_list(db, UNI_CHARS_GRAPH, "Introduce un caracter: ")
		case 2:
			display_sample_suggestion(db, UNI_CHARS_GRAPH, "Introduce un caracter: ")
		case 3:
			display_autocomplete_word(db, UNI_CHARS_GRAPH, "Introduce un caracter: ")
		case 4:
			main_char_menu(db)
		case 5:
			exit()
		case _:
			print("Entrada no reconocida.")
	
	uni_char_menu(db)

def bi_char_menu(db):
	print("---- Caracteres -- Elige una de las funcionalidades disponibles con BIGRAMAS ----")
	chosen = option_display(["Lista ordenada según probabilidad","Sugiere siguiente caracter","Autocompleta la palabra","Volver atrás", "Salir"])
	match chosen:
		case 1:
			display_recommend_list(db, BI_CHARS_GRAPH, "Introduce dos caracteres: ")
		case 2:
			display_sample_suggestion(db, BI_CHARS_GRAPH, "Introduce dos caracteres: ")
		case 3:
			display_autocomplete_word(db, BI_CHARS_GRAPH, "Introduce dos caracteres. O un caracter para indicar inicio de palabra: ")
		case 4:
			main_char_menu(db)
		case 5:
			exit()
		case _:
			print("Entrada no reconocida.")
	
	bi_char_menu(db)

def tri_char_menu(db):
	print("---- Caracteres -- Elige una de las funcionalidades disponibles con TRIGRAMAS ----")
	chosen = option_display(["Lista ordenada según probabilidad","Sugiere siguiente caracter","Autocompleta la palabra","Volver atrás", "Salir"])
	match chosen:
		case 1:
			display_recommend_list(db, TRI_CHARS_GRAPH, "Introduce tres caracteres: ")
		case 2:
			display_sample_suggestion(db, TRI_CHARS_GRAPH, "Introduce tres caracteres: ")
		case 3:
			display_autocomplete_word(db, TRI_CHARS_GRAPH, "Introduce tres caracteres. O dos caracteres para indicar inicio de palabra: ")
		case 4:
			main_char_menu(db)
		case 5:
			exit()
		case _:
			print("Entrada no reconocida.")
	
	tri_char_menu(db)

def uni_word_menu(db):
	print("---- Palabras -- Elige una de las funcionalidades disponibles con UNIGRAMAS ----")
	chosen = option_display(["Lista por probabilidades de aparición","Sugiere una palabra","Camino más probable entre dos palabras", "Camino más probable dado tamaño maximo", "Volver atrás", "Salir"])
	match chosen:
		case 1:
			display_recommend_list(db, UNI_WORDS_GRAPH, "Introduce una palabra: ")
		case 2:
			display_sample_suggestion(db, UNI_WORDS_GRAPH, "Introduce una palabra: ")
		case 3:
			unigram_path_two_words(db)
		case 4:
			display_most_likely_phrase(db, UNI_WORDS_GRAPH, "Introduce una palabra que inicie la frase: ")
		case 5:
			main_word_menu(db)
		case 6:
			exit()
		case _:
			print("Entrada no reconocida.")
	
	uni_word_menu(db)
			

def bi_word_menu(db):
	print("---- Palabras -- Elige una de las funcionalidades disponibles con BIGRAMAS ----")
	chosen = option_display(["Lista por probabilidades de aparición","Sugiere una palabra dado un bigrama","Camino más probable dado tamaño maximo", "Volver atrás", "Salir"])
	match chosen:
		case 1:
			display_recommend_list(db, BI_WORDS_GRAPH, "Introduce dos palabras separadas por un espacio: ")
		case 2:
			display_sample_suggestion(db, BI_WORDS_GRAPH, "Introduce dos palabras separadas por un espacio: ")
		case 3:
			display_most_likely_phrase(db, BI_WORDS_GRAPH, "Introduce dos palabras separadas por un espacio: ")
		case 4:
			main_word_menu(db)
		case 5:
			exit()
		case _:
			print("Entrada no reconocida.")

	bi_word_menu(db)

def tri_word_menu(db):
	print("---- Palabras -- Elige una de las funcionalidades disponibles con TRIGRAMAS ----")
	chosen = option_display(["Lista por probabilidades de aparición","Sugiere una palabra dado un trigrama", "Camino más probable dado tamaño maximo", "Volver atrás", "Salir"])
	match chosen:
		case 1:
			display_recommend_list(db, TRI_WORDS_GRAPH, "Introduce tres palabras separadas por espacios: ")
		case 2:
			display_sample_suggestion(db, TRI_WORDS_GRAPH, "Introduce tres palabras separadas por espacios: ")
		case 3:
			display_most_likely_phrase(db, TRI_WORDS_GRAPH, "Introduce tres palabras separadas por espacios: ")
		case 4:
			main_word_menu(db)
		case 5:
			exit()
		case _:
			print("Entrada no reconocida.")
	
	tri_word_menu(db)