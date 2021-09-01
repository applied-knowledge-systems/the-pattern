from pathlib import Path
import joblib

import ahocorasick

A = ahocorasick.Automaton()

datafile=Path('./data/words_cui.tsv')
with open(datafile,"r") as source:
    for line in source:
        word,cui=line.strip().split('\t')
        A.add_word(word, (cui, word))


A.make_automaton()
print(A.get_stats())

joblib.dump(A,"./automata/automata_syns.lzma")