def enable_debug():
    debug=execute('GET','debug{%s}'% hashtag())
    if debug=='1':
        debug=True
    else:
        debug=False
    return debug


def remove_prefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix):]

def filter_language(record):
    debug=enable_debug()
    from langdetect import detect
    #detect language of the article
    value=record['value']
    try:
        lang=detect(value[:1000])
        article_id = remove_prefix(record['key'],'paragraphs:') 
        if debug: 
            log(f"Success lang {article_id}",level='notice')
    except:
        lang=None
    return bool(lang=='en')

def parse_paragraphs(record):
    """
    parse paragraphs into sentences, returns list
    """
    debug=enable_debug()
    from sentence_splitter import SentenceSplitter
    splitter = SentenceSplitter(language='en')
    sentences=splitter.split(record['value'])
    article_id = remove_prefix(record['key'],'paragraphs:')
    pre = 'sentence:' + article_id 
    l = [{ 'key': f'{pre}','idx':f'{idx}','value': sentence } for idx,sentence in enumerate(sentences)]
    return l

"""
load symspell and relevant dictionaries
"""
sym_spell=None 

def load_symspell():
    import pkg_resources
    from symspellpy import SymSpell, Verbosity
    sym_spell = SymSpell(max_dictionary_edit_distance=1, prefix_length=7)
    dictionary_path = pkg_resources.resource_filename(
        "symspellpy", "frequency_dictionary_en_82_765.txt")
    bigram_path = pkg_resources.resource_filename(
        "symspellpy", "frequency_bigramdictionary_en_243_342.txt")
    # term_index is the column of the term and count_index is the
    # column of the term frequency
    sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)
    sym_spell.load_bigram_dictionary(bigram_path, term_index=0, count_index=2)
    return sym_spell

def spellcheck_sentences(sentence):
    """
    spellcheck each sentence
    """
    debug=enable_debug()
    global sym_spell
    if not sym_spell:
        sym_spell=load_symspell()

    suggestions = sym_spell.lookup_compound(sentence['value'], max_edit_distance=1,
                                        transfer_casing=True, ignore_non_words=True)

    value = suggestions[0].term
    if value:
        sentence['value']=value
        if debug: 
            log("Spellchecked sentence with article id %s" % sentence['key'])

    return sentence

def save_sentences(sentence):
    debug=enable_debug()
    article_id=sentence['key']
    idx=sentence['idx']
    sentence_key="%s:{%s}" % (article_id, hashtag())
    if debug: 
        log(f"Saving {sentence_key} and {idx}")
    try:
        execute('HSET', sentence_key,idx,sentence['value'])
        execute('SADD','processed_docs_stage2_para{%s}' % hashtag(),article_id)
    except:
        if debug:
            log(f"FAILURE: Saving {sentence_key} and {idx} failed")
        execute('SADD','processed_docs_stage2_failed{%s}' % hashtag(),article_id)
        
    


gb = GB('KeysReader')
gb.filter(filter_language)
gb.flatmap(parse_paragraphs)
gb.map(spellcheck_sentences)
gb.foreach(save_sentences)
gb.count()
gb.register('paragraphs:*',keyTypes=['string','hash'], mode="async_local")