
from transformers import AutoTokenizer, AutoModel
tokenizer = None
model= None  

def loadTokeniser():
    global tokenizer
    global model
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained("t5-small",torchscript=True)
    # Try RobertaTokenizerFast and BART
    # tokenizer = AutoTokenizer.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")
    model = AutoModel.from_pretrained('t5-small',torchscript=True)
    return tokenizer, model 

def remove_prefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix):]



def parse_sentence(record):
    import redisAI
    import numpy as np
    global tokenizer
    global model 
    if not tokenizer:
        tokenizer, model=loadTokeniser()

    article_text=[]
    for _, value in sorted(record['value'].items(), key=lambda item: int(item[0])):
        article_text.append(value)
    full_text=" ".join(article_text)
    inputs = tokenizer.encode_plus(full_text,max_length=512,add_special_tokens=True, return_tensors="np")

    input_ids = inputs['input_ids'].astype(np.int16)
    log(str(input_ids.shape))
    log(str(input_ids))
    # attention_mask = inputs['attention_mask']
    # token_type_ids = inputs['token_type_ids']
    key_prefix='sentence:'
    article_key=remove_prefix(record['key'],key_prefix)
    token_key = f"tokenized:T5:sum:{article_key}"
    tensor=redisAI.createTensorFromBlob('INT16', input_ids.shape, input_ids.tobytes())
    redisAI.setTensorInKey(token_key, tensor)
    execute('SADD','processed_docs_stage3_sum', token_key)

gb = GB()
gb.foreach(parse_sentence)
gb.count()
gb.run('sentence:*')