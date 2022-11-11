This project implements a n-gram language model on top of graph oriented database.

To run this project, it is mandatory to have installed docker and python on your system.

Built-in python libraries used:
- itertools
- os
- sys
- hashlib

To run main.py script on your computer here it is a step list:

1. Build and run a docker container as specified on the dockerfile. This docker will contain a ArandoDB

2. Install specified python libraries:
- python-arango
- python-dotenv
- sciPy

3. Create .env file at root level of your project folder. On this .env file you will need to specify the ABSOLUTE PATH of the books (.txt format on ANSI character encoding) used to train the model. Here is an example of how to do it, please take into account that the name of the env variables should remain the same as 
specified or else you will have to change these names on main.py script.

```
BOOK_1 = C:\Users\username\Desktop\TFG\bachelor-thesis\books\actas_capitulares_21_25.txt
BOOK_2 = C:\Users\username\Desktop\TFG\bachelor-thesis\books\al_primer_vuelo.txt
...
BOOK_14 = C:\Users\username\Desktop\TFG\bachelorThesis\books\la_regenta.txt
```

4. Run main.py using python.

To execute the GUI in the script demo.py:

1. Train the model, meaning that you will need to execute main.py in order to do this.

2. Install tkinter.

3. Run demo.py using python

To evaluate the model and calculate perplexity you will need to run evaluate.py:

1. Add to .env file the ABSOLUTE PATH of the books (.txt format on ANSI character encoding) used to test and train the model. Here is an example of how to do it, please take into account that the name of the env variables should remain the same as specified or else you will have to change these names on evaluate.py script.

```
TEST_1 = C:\Users\username\Desktop\TFG\bachelorThesis\books\lazarillo_de_tormes.txt
TEST_2 = C:\Users\username\Desktop\TFG\bachelorThesis\books\unico_hijo.txt
...
TEST_5 = C:\Users\username\Desktop\TFG\bachelorThesis\books\la_montalvez.txt
```

2. Install ntlk.

3. Run evaluate.py using python
