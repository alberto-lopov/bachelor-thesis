import re
import nltk
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk.lm import MLE
from nltk.lm import Laplace

import os, sys
sys.path.insert(0, os.getcwd())

from dotenv import load_dotenv
load_dotenv()

BOOK_1 = os.getenv('BOOK_1')
BOOK_2 = os.getenv('BOOK_2')
BOOK_3 = os.getenv('BOOK_3')
BOOK_4 = os.getenv('BOOK_4')
BOOK_5 = os.getenv('BOOK_5')
BOOK_6 = os.getenv('BOOK_6')
BOOK_7 = os.getenv('BOOK_7')
BOOK_8 = os.getenv('BOOK_8')
BOOK_9 = os.getenv('BOOK_9')
BOOK_10 = os.getenv('BOOK_10')
BOOK_11 = os.getenv('BOOK_11')
BOOK_12 = os.getenv('BOOK_12')
BOOK_13 = os.getenv('BOOK_13')
BOOK_14 = os.getenv('BOOK_14')
TEST_1 = os.getenv('TEST_1')
TEST_2 = os.getenv('TEST_2')
TEST_3 = os.getenv('TEST_3')

from src.functions import clean_word
nltk.download('punkt')

def read_datasets(file_paths: list):
  if type(file_paths) != list:
    raise Exception("The argument specified it is not a list of string")

  book = 1
  for path in file_paths:
    #open text file
    print("---- Inicio Libro: " + str(book) + " ----")
    file = open(path)
    book_text = file.read()
    data_set = []

    raw_text = book_text.split(".")
    for sentence in raw_text:
      cleaned_sentence = ''
      array = re.findall(r'\b\w+\b', sentence)
      for word in array:
        cleaned_sentence = cleaned_sentence + clean_word(word) + ' '
      
      #If we pass empty arrays to mle fit we will find division by zero and crash the program
      if cleaned_sentence != '':
        data_set.append(cleaned_sentence[:-1])
  
    file.close()
    print("---- FIN Libro: " + str(book) + " ----")

    book += 1

  return data_set


def ngram_evaluation(n, train_sentences, test_sentences): 

  tokenized_text = [list(map(str.lower, nltk.tokenize.word_tokenize(sent, 'spanish'))) 
                  for sent in train_sentences]

  train_data, padded_vocab = padded_everygram_pipeline(n, tokenized_text)
  mle_prob = MLE(n)
  mle_prob.fit(train_data, padded_vocab)

  tokenized_text = [list(map(str.lower, nltk.tokenize.word_tokenize(sent, 'spanish'))) 
                  for sent in test_sentences]

  test_data, _ = padded_everygram_pipeline(n, tokenized_text)

  count_not_inf = 0
  sum_perplexity = 0
  count_inf = 0
  for sentence in test_data:
    perplexity = mle_prob.perplexity(sentence)
    if perplexity == float('inf'):
      count_inf += 1
    else:
      count_not_inf += 1
      sum_perplexity += perplexity

  print("MLE Perplexity " + str(n) + "-gram: " + str(sum_perplexity / count_not_inf) + " -- Number of inf: " + str(count_inf) + " -- Total Number: " + str(count_inf + count_not_inf))

def ngram_char_evaluation(n, train_sentences, test_sentences): 

  tokenized_text = [list(map(str.lower, [char for char in sent])) 
                  for sent in train_sentences]

  train_data, padded_vocab = padded_everygram_pipeline(n, tokenized_text)
  mle_prob = MLE(n)
  mle_prob.fit(train_data, padded_vocab)

  tokenized_text = [list(map(str.lower, [char for char in sent])) 
                  for sent in test_sentences]

  test_data, _ = padded_everygram_pipeline(n, tokenized_text)

  count_not_inf = 0
  sum_perplexity = 0
  count_inf = 0
  for sentence in test_data:
    perplexity = mle_prob.perplexity(sentence)
    if perplexity == float('inf'):
      count_inf += 1
    else:
      count_not_inf += 1
      sum_perplexity += perplexity

  print("MLE Perplexity " + str(n) + "-gram: " + str(sum_perplexity / count_not_inf) + " -- Number of inf: " + str(count_inf) + " -- Total Number: " + str(count_inf + count_not_inf))

def laplace_ngram_evaluation(n, train_sentences, test_sentences): 

  tokenized_text = [list(map(str.lower, nltk.tokenize.word_tokenize(sent, 'spanish'))) 
                  for sent in train_sentences]

  train_data, padded_vocab = padded_everygram_pipeline(n, tokenized_text)
  laplace_prob = Laplace(n)
  laplace_prob.fit(train_data, padded_vocab)

  tokenized_text = [list(map(str.lower, nltk.tokenize.word_tokenize(sent, 'spanish'))) 
                  for sent in test_sentences]

  test_data, _ = padded_everygram_pipeline(n, tokenized_text)

  count_not_inf = 0
  sum_perplexity = 0
  for sentence in test_data:
    perplexity = laplace_prob.perplexity(sentence)
    count_not_inf += 1
    sum_perplexity += perplexity

  print("LAPLACE Perplexity " + str(n) + "-gram: " + str(sum_perplexity / count_not_inf) )

def laplace_char_ngram_evaluation(n, train_sentences, test_sentences): 

  tokenized_text = [list(map(str.lower, [char for char in sent])) 
                  for sent in train_sentences]

  train_data, padded_vocab = padded_everygram_pipeline(n, tokenized_text)
  laplace_prob = Laplace(n)
  laplace_prob.fit(train_data, padded_vocab)

  tokenized_text = [list(map(str.lower, [char for char in sent])) 
                  for sent in test_sentences]

  test_data, _ = padded_everygram_pipeline(n, tokenized_text)

  count_not_inf = 0
  sum_perplexity = 0
  for sentence in test_data:
    perplexity = laplace_prob.perplexity(sentence)
    count_not_inf += 1
    sum_perplexity += perplexity

  print("LAPLACE Perplexity " + str(n) + "-gram: " + str(sum_perplexity / count_not_inf) )

train_sentences = read_datasets([BOOK_1, BOOK_2, BOOK_3, BOOK_4, BOOK_5, BOOK_6, BOOK_7, BOOK_8, BOOK_9, BOOK_10, BOOK_11, BOOK_12, BOOK_13, BOOK_14])
test_sentences = read_datasets([TEST_1, TEST_2, TEST_3])

ngram_evaluation(1, train_sentences, test_sentences)
ngram_evaluation(2, train_sentences, test_sentences)
ngram_evaluation(3, train_sentences, test_sentences)
ngram_char_evaluation(1, train_sentences, test_sentences)
ngram_char_evaluation(2, train_sentences, test_sentences)
ngram_char_evaluation(3, train_sentences, test_sentences)
laplace_ngram_evaluation(1, train_sentences, test_sentences)
laplace_ngram_evaluation(2, train_sentences, test_sentences)
laplace_ngram_evaluation(3, train_sentences, test_sentences)
laplace_char_ngram_evaluation(1, train_sentences, test_sentences)
laplace_char_ngram_evaluation(2, train_sentences, test_sentences)
laplace_char_ngram_evaluation(3, train_sentences, test_sentences)
