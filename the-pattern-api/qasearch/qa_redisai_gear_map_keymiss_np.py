### This gears will use pre-computed answers all sentences using BERT tokenizer for QA, run QA model and cache results.
### and you can still keep writing into redis thanks to async/await 


tokenizer = None 


def loadTokeniser():
    global tokenizer
    from transformers import BertTokenizerFast
    tokenizer = BertTokenizerFast.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
    return tokenizer

def to_np(rai_tensor, data_type):
    import numpy as np
    import redisAI
    t=np.frombuffer(redisAI.tensorGetDataAsBlob(rai_tensor), dtype=data_type).reshape(redisAI.tensorGetDims(rai_tensor))
    return t


async def qa_cached_keymiss(record):
    val=record['key'].split('_')
    cache_key='bertqa{%s}_%s_%s' % (hashtag(), val[1],val[2])
    log("QA cached called from keymiss")
    res = await qa(val)
    log("Result "+str(res))
    log("Cache key "+str(cache_key))
    execute('set',cache_key, res)
    override_reply(res)
    return res


async def qa(record):
    log("Called with "+ str(record))
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
    t=redisAI.getTensorFromKey(token_key)
    input_ids_context=to_np(t,np.int64)
    input_ids = np.append(input_ids_question,input_ids_context)
    attention_mask = np.array([[1]*len(input_ids)])
    input_idss=np.array([input_ids])
    num_seg_a=input_ids_question.shape[1]
    num_seg_b=input_ids_context.shape[0]
    token_type_ids = np.array([0]*num_seg_a + [1]*num_seg_b)
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
    answer_start_scores=to_np(res[0],np.float32)
    answer_end_scores = to_np(res[1],np.float32)
    answer_start = np.argmax(answer_start_scores)
    answer_end = np.argmax(answer_end_scores) + 1
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end],skip_special_tokens = True))
    log("Answer "+str(answer))
    return answer

gb = GB('KeysReader')
gb.map(qa_cached_keymiss)
gb.register(prefix='bertqa*', commands=['get'], eventTypes=['keymiss'], mode="async_local")
