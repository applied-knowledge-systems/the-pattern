"""
This version reads directly from RRF UMLS dump
without any pre-processing
Download UMLS methathesaurus 
and adjust path to datafile to MRXW_ENG.RRF

"""
from pathlib import Path
from test_automata import Automata
from spacy.lang.en import stop_words as sw

import joblib

import ahocorasick
import re

stop_words = sw.STOP_WORDS
def is_stop_word(w):
    return w.lower() in stop_words

non_alpha_re = re.compile("^[^a-zA-Z0-9].*$")
def is_non_alpha(w):
    return re.match(non_alpha_re, w) is not None

def is_all_caps(w):
    return w.upper() == w


assert(is_stop_word("is"))
assert(is_non_alpha("-"))
assert(is_all_caps("AIDS"))
assert(not is_all_caps("hearing"))

t = ahocorasick.Automaton()

datafile=Path('/home/alex/py_code/the-pattern/data/2019AB/META/MRXW_ENG.RRF')
with open(datafile,"r") as source:
    for line in source:
        _, term, cui,_, _,_=line.strip().split('|')
        if t.exists(term) or len(term)<4 or is_stop_word(term) or is_non_alpha(term):
            continue
        if not is_all_caps(term):
            term = term.lower()
        if term and cui:
            # t.add_word(term, cui)
            t.add_word(term, (cui, term))
            
        else:
            print("Error ",term)


t.make_automaton()

joblib.dump(t,"./automata/automata_fresh.pkl")