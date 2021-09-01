import pickle 
import redis 
import torch 

from transformers import T5ForConditionalGeneration, T5Tokenizer

def log_gpu(device):
    #Additional Info when using cuda
    if device.type == 'cuda':
        print(torch.cuda.get_device_name(0))
        print('Memory Usage:')
        print('Allocated:', round(torch.cuda.memory_allocated(0)/1024**3,1), 'GB')
        print('Cached:   ', round(torch.cuda.memory_reserved(0)/1024**3,1), 'GB')

def main():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print('Using device:', device)
    print()
    redis_client=redis.Redis(host='10.144.17.211',port=9001)
    model = T5ForConditionalGeneration.from_pretrained("t5-base")
    model=model.to(device)
    tokenizer = T5Tokenizer.from_pretrained("t5-base")
    tokens_set=redis_client.smembers("processed_docs_stage3_queue")
    for t in tokens_set:
        tokens=pickle.loads(redis_client.get(t))
        tens=torch.tensor([tokens]).to(device)
        log_gpu(device)
        outputs = model.generate(tens, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
        output = tokenizer.decode(outputs[0], skip_special_tokens=True)
        head,*tail=t.decode().split(":")
        article_id=tail[0]
        redis_client.hset(f"article_id:{article_id}",mapping={'summary': output})
        print(f"Summary build for {article_id} and {output}")
        redis_client.srem("processed_docs_stage3_queue",t)


if __name__ == "__main__":
    main()
