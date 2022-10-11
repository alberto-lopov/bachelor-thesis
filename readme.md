To run this project, it is mandatory to have installed docker and python on your system.

To run this script on your computer here it is a step list:

1. Build and run a docker container as specified on the dockerfile. This docker will contain a ArandoDB

2. Install specified python libraries:
- python-arango
- python-dotenv
- sciPy

3. Create .env file at root level of your project folder. On this .env file you will need to specify the ABSOLUTE PATH of the books (.txt format)
use to train the model. Here is an example of how to do it, please take into account that the name of the env variables should remain the same as 
specified or else you will have to change these names on main.py script.

```
BOOK_1 = C:\Users\username\Desktop\TFG\bachelor-thesis\books\actas_capitulares_21_25.txt
BOOK_2 = C:\Users\username\Desktop\TFG\bachelor-thesis\books\al_primer_vuelo.txt
...
BOOK_10 = C:\Users\username\Desktop\TFG\bachelor-thesis\books\amar_es_vencer.txt
```

4. Run main.py using python.