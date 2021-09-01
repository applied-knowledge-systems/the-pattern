
summarization = None

def loadSummarization():
    from transformers import pipeline
    global summarization
    summarization = pipeline("summarization", model="facebook/bart-large-xsum", tokenizer="facebook/bart-large-xsum")
    return summarization

def remove_prefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix):]



def parse_sentence(record):
    global summarization
    if not summarization:
        summarization=loadSummarization()

    article_text=[]
    for _, value in sorted(record['value'].items(), key=lambda item: int(item[0])):
        article_text.append(value)
    full_text=" ".join(article_text[0:512])
    summary_text = summarization(full_text)[0]['summary_text']
    key_prefix='sentence:'
    article_key=remove_prefix(record['key'],key_prefix)
    summary_key = f"summary:{article_key}"
    execute('SET', summary_key, summary_text)
    execute('SADD','processed_docs_stage3_sum', inputs)

gb = GB()
gb.foreach(parse_sentence)
gb.count()
gb.run('sentence:*')