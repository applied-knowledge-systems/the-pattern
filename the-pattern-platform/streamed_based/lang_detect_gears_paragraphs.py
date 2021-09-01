from langdetect import detect   

def remove_prefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix):]

def detect_language(record):
    #detect language of the article
    value=record['value']
    try:
        lang=detect(value[:1000])
    except:
        lang="empty"
    if lang=='en':
        article_id = remove_prefix(record['key'],'paragraphs:') 
        log(f"Success lang {article_id}",level='notice')
        execute('XADD', 'lang_eng{%s}' % hashtag(), '*', 'article_id', f"{article_id}","content",f"{value}")
    else:
        log("Failed to detect language, deleting: "+str(record['key']),level='notice')
        execute('DEL', record['key'])


gb = GB('KeysReader')
gb.foreach(detect_language)
gb.count()
gb.register('paragraphs:*',keyTypes=['string'], mode="async_local")