nlp = None

def load_nlp_object():
    import en_core_web_sm
    log("Importing NLP")
    nlp = en_core_web_sm.load(disable=['ner','tagger'])
    nlp.max_length=1200000
    return nlp


def OnRegistered():
    global nlp
    nlp=load_nlp_object()
    return nlp


def remove_prefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix):]

def parse_paragraphs(x):
    global nlp
    article_id=x['value']['article_id']
    paragraphs =x['value']['content']
    if not nlp:
        nlp=load_nlp_object()
    doc=nlp(paragraphs)
    idx=1
    for each_sent in doc.sents:
        sentence_key="sentences:%s:%s:{%s}" % (article_id, idx, hashtag())
        execute('SET', sentence_key, each_sent)
        idx+=1
        execute('XADD', 'sentences_tospellcheck{%s}' % hashtag(), '*', 'sentence_key', f"{sentence_key}",'content', f"{each_sent}")
        log(f"Successfully processed paragraphs {sentence_key}",level='notice')
    
gb = GearsBuilder('StreamReader')
gb.foreach(parse_paragraphs)
gb.register('lang_eng*', batch=1, mode="async_local", onRegistered=OnRegistered, onFailedPolicy='continue', trimStream=True)

