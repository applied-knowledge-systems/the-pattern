sym_spell=None 

def load_symspell():
    import pkg_resources
    from symspellpy import SymSpell, Verbosity
    sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
    dictionary_path = pkg_resources.resource_filename(
        "symspellpy", "frequency_dictionary_en_82_765.txt")
    bigram_path = pkg_resources.resource_filename(
        "symspellpy", "frequency_bigramdictionary_en_243_342.txt")
    # term_index is the column of the term and count_index is the
    # column of the term frequency
    sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)
    sym_spell.load_bigram_dictionary(bigram_path, term_index=0, count_index=2)
    return sym_spell

def OnRegisteredSym():
    global sym_spell
    sym_spell=load_symspell()
    return sym_spell



def symspell_sentences(record):
    global sym_spell
    if not sym_spell:
        sym_spell=load_symspell()

    sentence_key=record['value']['sentence_key']
    sentence_orig=record['value']['content']
    # shard_id=hashtag()
    # log(f"Spellchecker received {sentence_key} and my {shard_id}")
    # max edit distance per lookup (per single word, not per whole input string)
    suggestions = sym_spell.lookup_compound(sentence_orig, max_edit_distance=2,
                                        transfer_casing=True, ignore_non_words=True)


    value = suggestions[0].term
    if value:
        execute('XADD', 'sentence_to_tokenise_{%s}' % hashtag(), '*', 'sentence_key', f"{sentence_key}",'content',f"{value}")
        log("Successfully spellchecked sentence "+str(sentence_key),level='notice')
    else:
        execute('SADD','spelling_screw_ups{%s}' % hashtag(), sentence_key)


bg = GearsBuilder('StreamReader')
bg.foreach(symspell_sentences)
bg.register('sentences_tospellcheck*', batch=1, mode="async_local",onRegistered=OnRegisteredSym, onFailedPolicy='continue', trimStream=True)
