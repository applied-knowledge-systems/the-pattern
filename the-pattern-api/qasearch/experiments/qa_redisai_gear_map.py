### This gears will use pre-computed answers all sentences using BERT tokenizer for QA, run QA model and cache results.
### and you can still keep writing into redis thanks to async/await 


tokenizer = None 

def loadTokeniser():
    global tokenizer
    from transformers import BertTokenizerFast
    tokenizer = BertTokenizerFast.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
    return tokenizer

def to_np(rai_tensor, data_type):
  return np.frombuffer(redisAI.tensorGetDataAsBlob(rai_tensor), dtype=data_type).reshape(redisAI.tensorGetDims(rai_tensor))


async def qa_cached(record):
    cache_key='cache_{%s}_{%s}_{%s}' % (hashtag(), record[1],record[2])
    res = execute('get', cache_key)
    log("QA cached called")
    log("RECORD %s" % str(record) )
    if res:
        log("Cache hit")
        log(str(res))
        return res
    res = await qa(record)
    execute('set',cache_key, res)
    return res


async def qa(record):
    log("Called with "+ str(record))
    log("Trigger "+str(record[0]))
    log("Key "+ str(record[1]))
    log("Question  "+ str(record[2]))

    global tokenizer

    import redisAI
    import numpy as np

    sentence_key=record[1]
    question=record[2]
    hash_tag="{%s}" % hashtag()
    log("Shard_id "+hash_tag)
    if not tokenizer:
        tokenizer=loadTokeniser()

     

    token_key = f"tokenized:bert:qa:{sentence_key}"

    input_ids_question = tokenizer.encode(question, add_special_tokens=True, truncation=True, return_tensors="np")
    log("Input ids question "+str(input_ids_question))
    log("Input ids question shape"+str(input_ids_question.shape))
    log("Input ids question shape"+str(input_ids_question.dtype))
    t=redisAI.getTensorFromKey(token_key)
    input_ids_context=np.frombuffer(redisAI.tensorGetDataAsBlob(t), dtype=np.int64).reshape(redisAI.tensorGetDims(t))
    log("Input ids context "+str(input_ids_context))
    log("Input ids content shape "+str(input_ids_context.shape))
    log("Input ids content dtype "+str(input_ids_context.dtype))
    input_ids = np.append(input_ids_question,input_ids_context)
    
    log("Combined input_ids shape"+ str(input_ids.shape))
    attention_mask = np.array([[1]*len(input_ids)])
    input_idss=np.array([input_ids])
    log("input ids "+ str(input_idss.shape))
    log("Attention mask shape "+str(attention_mask.shape))
    num_seg_a=input_ids_question.shape[1]
    log(str(num_seg_a))
    num_seg_b=input_ids_context.shape[0]
    # num_seg_b=redisAI.tensorGetDims(input_ids_context)[0]
    log("Tensor get dims "+str(num_seg_b))
    token_type_ids = np.array([0]*num_seg_a + [1]*num_seg_b)
    log("Segments id "+str(token_type_ids.shape))
    modelRunner = redisAI.createModelRunner(f'bert-qa{hash_tag}')

    input_idss_ts=redisAI.createTensorFromBlob('INT64', input_idss.shape, input_idss.tobytes())
    attention_mask_ts=redisAI.createTensorFromBlob('INT64', attention_mask.shape, attention_mask.tobytes())
    token_type_ids_ts=redisAI.createTensorFromBlob('INT64', token_type_ids.shape, token_type_ids.tobytes())
    redisAI.modelRunnerAddInput(modelRunner, 'input_ids', input_idss_ts)
    redisAI.modelRunnerAddInput(modelRunner, 'attention_mask', attention_mask_ts)
    redisAI.modelRunnerAddInput(modelRunner, 'token_type_ids', token_type_ids_ts)
    redisAI.modelRunnerAddOutput(modelRunner, 'answer_start_scores')
    redisAI.modelRunnerAddOutput(modelRunner, 'answer_end_scores')
    res = await redisAI.modelRunnerRunAsync(modelRunner)
    # redisAI.setTensorInKey('c{1}', res[0])
    log(str(res[0]))
    log("answer end"+str(res[1]))

    log(f"Model run on {hash_tag}")
    answer_start_scores=np.frombuffer(redisAI.tensorGetDataAsBlob(res[0]), dtype=np.float32).reshape(redisAI.tensorGetDims(res[0]))
    # answer_start_scores = res[0]
    answer_end_scores = np.frombuffer(redisAI.tensorGetDataAsBlob(res[1]), dtype=np.float32).reshape(redisAI.tensorGetDims(res[1]))
    log("Answer start scores type " +str(type(answer_start_scores)))
    answer_start = np.argmax(answer_start_scores)
    answer_end = np.argmax(answer_end_scores) + 1
    log("Answer start "+str(answer_start))
    log("Answer end "+str(answer_end))
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end],skip_special_tokens = True))
    return answer


gb = GB('CommandReader')
gb.map(qa_cached)
gb.register(trigger='RunQABERT',mode="async_local")