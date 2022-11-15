This project implements a n-gram language model on top of [ArangoDB](https://www.arangodb.com/docs/devel/).
# Introduction

This repository is a n-gram based language model. It is built using graphs as its data structure.

This system, called GPG - Generative Pre-trained Graph, is composed by a word-level language model and a char-level language model.

The purpose of this sistem is to provide suggestions to a user writing a text on spanish.

It doesn´t try to produce large text with a given input, instead its suggestions are focused on trying to give the next word, auto-complete word, and produce little size phrases with some given imput.

To interact with the system you can run:
 - demo.py: GUI that will show suggestions to a user typing something on spanish
 - main.py: Terminal based interface that allows to interact with each submodel implemented and all ot its functions
 - evaluate.py: Will output perplexity metric of the data corpus used to train and test the model.

This project is my bachelor thesis to finish my studies on Software Engineering at UGR.
If you want to have a look into the details of this project i suggest you to read the documentation uploaded in this repository. (At this moment only spanish documentation is avalaible)
# Instructions

To run this project, it is mandatory to have installed docker and python on your system.

Built-in python libraries used:
- itertools
- os
- sys
- hashlib

## Main.py

To run main.py script on your computer here it is a step list:

1. Build and run a docker container as specified on the dockerfile. This docker will contain a ArandoDB

2. Install specified python libraries:
- [python-arango](https://docs.python-arango.com/en/main/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [sciPy](https://scipy.org/)

3. Create .env file at root level of your project folder. On this .env file you will need to specify the ABSOLUTE PATH of the books (.txt format on ANSI character encoding) used to train the model. Here is an example of how to do it, please take into account that the name of the env variables should remain the same as 
specified or else you will have to change these names on main.py script.

```
BOOK_1 = C:\Users\username\Desktop\TFG\bachelor-thesis\books\actas_capitulares_21_25.txt
BOOK_2 = C:\Users\username\Desktop\TFG\bachelor-thesis\books\al_primer_vuelo.txt
...
BOOK_14 = C:\Users\username\Desktop\TFG\bachelorThesis\books\la_regenta.txt
```

4. Run main.py using python.

## Demo.py

To execute the GUI in the script demo.py:

1. Train the model, meaning that you will need to execute main.py in order to do this.

2. Install [tkinter](https://docs.python.org/es/3/library/tkinter.html).

3. Run demo.py using python

## Evaluate.py

To evaluate the model and calculate perplexity you will need to run evaluate.py:

1. Add to .env file the ABSOLUTE PATH of the books (.txt format on ANSI character encoding) used to test and train the model. Here is an example of how to do it, please take into account that the name of the env variables should remain the same as specified or else you will have to change these names on evaluate.py script.

```
TEST_1 = C:\Users\username\Desktop\TFG\bachelorThesis\books\lazarillo_de_tormes.txt
TEST_2 = C:\Users\username\Desktop\TFG\bachelorThesis\books\unico_hijo.txt
...
TEST_5 = C:\Users\username\Desktop\TFG\bachelorThesis\books\la_montalvez.txt
```

2. Install [ntlk](https://www.nltk.org/).

3. Run evaluate.py using python
