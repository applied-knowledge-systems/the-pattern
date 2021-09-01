### This gears will pre-compute (encode) all sentences using BERT tokenizer for QA

tokenizer = None 

def loadTokeniser():
    global tokenizer
    from transformers import BertTokenizerFast
    tokenizer = BertTokenizerFast.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
    # tokenizer = AutoTokenizer.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")
    return tokenizer

def remove_prefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix):]



def parse_sentence(record):
    import redisAI
    import numpy as np
    global tokenizer
    if not tokenizer:
        tokenizer=loadTokeniser()
    hash_tag="{%s}" % hashtag()

    for idx, value in sorted(record['value'].items(), key=lambda item: int(item[0])):
        tokens = tokenizer.encode(value, add_special_tokens=False, max_length=511, truncation=True, return_tensors="np")
        tokens = np.append(tokens,tokenizer.sep_token_id).astype(np.int64) 
        tensor=redisAI.createTensorFromBlob('INT64', tokens.shape, tokens.tobytes())
        
        key_prefix='sentence:'
        sentence_key=remove_prefix(record['key'],key_prefix)
        token_key = f"tokenized:bert:qa:{sentence_key}:{idx}"
        # execute('SET', token_key, tokens)
        redisAI.setTensorInKey(token_key, tensor)
        execute('SADD',f'processed_docs_stage3_tokenized{hash_tag}', token_key)

gb = GB()
gb.foreach(parse_sentence)
gb.count()
gb.run('sentence:*',keyTypes=['hash'])