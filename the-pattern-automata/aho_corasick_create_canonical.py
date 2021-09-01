"""
This version reads directly from RRF UMLS dump
without any pre-processing
Download UMLS methathesaurus 
and adjust path to datafile to MRXW_ENG.RRF

"""
from pathlib import Path
import httpimport
with httpimport.remote_repo(['stop_words'], "https://raw.githubusercontent.com/explosion/spaCy/master/spacy/lang/en/"):
    import stop_words
    from stop_words import STOP_WORDS

import joblib

import ahocorasick
import re

def is_stop_word(w):
    return w.lower() in STOP_WORDS

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
counter=0
datafile=Path('./data/canonical_sorted.tsv')
with open(datafile,"r") as source:
    for line in source:
        term, cui=line.strip().split('\t')
        # t.exists(term) prevents adding the same key
        if len(term)<4 or is_stop_word(term) or is_non_alpha(term):
            continue
        if not is_all_caps(term):
            term = term.lower()
        if term and cui:
            # t.add_word(term, cui)
            t.add_word(term, (cui, term))
            counter+=1
            
        else:
            print("Error ",term)

print(f"Added {counter}")
t.make_automaton()

joblib.dump(t,"./automata/automata_fresh_canonical.pkl")