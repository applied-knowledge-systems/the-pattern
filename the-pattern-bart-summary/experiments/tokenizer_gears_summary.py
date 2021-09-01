
tokenizer = None
model= None  

def loadTokeniser():
    global tokenizer
    global model
    import torch
    from transformers import AutoTokenizer, T5ForConditionalGeneration
    tokenizer = AutoTokenizer.from_pretrained("t5-small")
    # Try RobertaTokenizerFast and BART
    # tokenizer = AutoTokenizer.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")
    model = T5ForConditionalGeneration.from_pretrained("t5-small")
    return tokenizer, model 

def remove_prefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix):]



def parse_sentence(record):

    global tokenizer
    global model 
    if not tokenizer:
        tokenizer, model=loadTokeniser()

    article_text=[]
    for _, value in sorted(record['value'].items(), key=lambda item: int(item[0])):
        article_text.append(value)
    full_text=" ".join(article_text[0:512])
    inputs = tokenizer.encode("summarize: " + full_text, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    key_prefix='sentence:'
    article_key=remove_prefix(record['key'],key_prefix)
    summary_key = f"summary:T5:{article_key}"
    execute('SET', summary_key, output)
    execute('SADD','processed_docs_stage3_sum', summary_key)

gb = GB()
gb.foreach(parse_sentence)
gb.count()
gb.run('sentence:*')