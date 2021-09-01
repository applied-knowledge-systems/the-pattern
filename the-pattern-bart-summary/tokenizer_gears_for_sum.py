
tokenizer = None
rconn=None

def connecttoRedis():
    import redis 
    redis_client=redis.Redis(host='redisgraph',port=6379,charset="utf-8", decode_responses=True)
    return redis_client


def loadTokeniser():
    global tokenizer
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained("t5-base")
    # Try RobertaTokenizerFast and BART
    # tokenizer = AutoTokenizer.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")
    return tokenizer

def remove_prefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix):]



def parse_sentence(record):
    global tokenizer
    if not tokenizer:
        tokenizer=loadTokeniser()
    
    global rconn
    if not rconn:
        rconn=connecttoRedis()

    import pickle
    key_prefix='sentence:'
    article_key=remove_prefix(record['key'],key_prefix)
    if not rconn.sismember('processed_docs_stage3_arts', article_key):
        article_text=[]
        for _, value in sorted(record['value'].items(), key=lambda item: int(item[0])):
            article_text.append(value)
        full_text=" ".join(article_text)
        inputs = tokenizer.encode("summarize: " + full_text, max_length=512, truncation=True)
        

        summary_key = f"summary_T5:{article_key}"
        rconn.set(summary_key, pickle.dumps(inputs))
        rconn.sadd('processed_docs_stage3_queue', summary_key)
        rconn.sadd('processed_docs_stage3_arts', article_key)
    else:
        log(f"Already processed article {article_key}")

gb = GB()
gb.foreach(parse_sentence)
gb.count()
gb.run('sentence:*')