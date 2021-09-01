"""
specially prepared sorted STR to CUI dump:
sudo mysql --skip-column-names  --raw umls_meta  -e "select STR, CUI from MRCONSO where LAT='ENG' AND TS='P' AND STT='PF' AND ISPREF='Y' ORDER BY CHAR_LENGTH(STR);" > canonical_sorted.tsv

"""
from pathlib import Path
import httpimport
with httpimport.remote_repo(['stop_words'], "https://raw.githubusercontent.com/explosion/spaCy/master/spacy/lang/en/"):
    import stop_words
    from stop_words import STOP_WORDS

import joblib

import ahocorasick
import re

from string import punctuation

regex = re.compile('[%s]' % re.escape(punctuation))

def remove_punct(w):
    return regex.sub('', w)
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
        for each_token in term.split(" "):
            each_token=remove_punct(each_token)
            if t.exists(term) or len(each_token)<4 or is_stop_word(each_token) or is_non_alpha(each_token):
                if counter % 100 == 0:
                    print(f"Token skipped {each_token} for {cui}")
                continue
            if is_all_caps(each_token):
                each_token = each_token.lower()
            t.add_word(each_token, (cui, term))
            counter+=1

print(f"Added {counter}")
t.make_automaton()

joblib.dump(t,"./automata/automata_fresh_sorted.pkl")