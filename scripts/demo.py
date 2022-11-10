import os, sys
sys.path.insert(0, os.getcwd())

import threading
import time
from tkinter import *
from arango import ArangoClient

from src.constants import DB_NAME, URL_ARANGO_DB
from src.functions import autoword_suggestions, next_word_suggestion
# Initialize the client for ArangoDB.
client = ArangoClient(hosts=URL_ARANGO_DB)
sys_db = client.db("_system", username="root")
db = client.db(DB_NAME, username="root")
option_dict = {}

#Decorator that will debounce a function so that it is called after "wait" seconds
#If it is called multiple times, will wait for the last call to be debounced and run only this one.
def debounce(wait):

    def decorator(fn):
        def debounced(*args, **kwargs):
            def call_it():
                debounced._timer = None
                debounced._last_call = time.time()
                return fn(*args, **kwargs)

            time_since_last_call = time.time() - debounced._last_call
            if time_since_last_call >= wait:
                return call_it()

            if debounced._timer is None:
                debounced._timer = threading.Timer(wait - time_since_last_call, call_it)
                debounced._timer.start()

        debounced._timer = None
        debounced._last_call = 0

        return debounced

    return decorator

# Function to update the list of options given
def update_words(new_options):
    option_word_frame.delete(0, END)

    used_options = []
    for option in new_options.values():
        if option not in used_options and option != '':
            option_word_frame.insert(END, option)
            used_options.append(option)

def update_chars(new_options):
    option_char_frame.delete(0, END)

    used_options = []
    for option in new_options.values():
        if option not in used_options and option != '':
            option_char_frame.insert(END, option)
            used_options.append(option)

# Event handlers when selection a option
def fillout_word(e):
    last_sentence = input_box.get()
    input_box.delete(0, END)

    input_box.insert(0, last_sentence.strip() + " " + option_word_frame.get(ANCHOR))

def fillout_char(e):
    last_sentence = input_box.get()
    input_box.delete(0, END)
   
    input_box.insert(0, last_sentence.strip() + (option_char_frame.get(ANCHOR)).split('-')[-1])

#Event handler debounced 1 seconds that queries the DB.
@debounce(1)
def check(e):
    typed = input_box.get()
    new_word_options = {}
    new_char_options = {}

    if typed != '':
        new_word_options = next_word_suggestion(db, typed)
        new_char_options = autoword_suggestions(db, typed)

    update_words(new_word_options)
    update_chars(new_char_options)

# ---------------------------- Tkinter Widgets ----------------------------
root = Tk()
root.title("Demo GPG")
root.geometry("800x600")

input_title = Label(root, text = "Empieza a escribir... ", font=("Roboto", 12), fg = "grey")
input_title.pack(pady=20)

input_box = Entry(root, font=("Roboto", 12), width=60)
input_box.pack(pady = 10)

option_word_frame = Listbox(root, width=50, height=4)
option_word_frame.pack(pady=40)

option_char_frame = Listbox(root, width=50, height=4)
option_char_frame.pack(pady=10)

#Event binding
option_word_frame.bind("<<ListboxSelect>>", fillout_word)
option_char_frame.bind("<<ListboxSelect>>", fillout_char)
input_box.bind("<KeyRelease>", check)

root.mainloop()

# Close connection with Database
client.close()