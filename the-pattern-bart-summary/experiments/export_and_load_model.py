from transformers import BartForConditionalGeneration
from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch
from redisai import ClusterClient
from transformers import AutoTokenizer
import numpy as np

class MyModel(T5ForConditionalGeneration):
  def __init__(self,kwargs):
    super(MyModel, self).__init__(kwargs) # could be other init params

  def forward(self, params):
    self.generate(params)


pb = torch.jit.trace(model, inputs)

def export_bert():
    text = """At a very high level, one of the most critical steps in any ML pipeline is called AI serving, a task usually performed by an AI inference engine. The AI inference engine is responsible for the model deployment and performance monitoring steps in the figure above, and represents a whole new world that will eventually determine whether applications can use AI technologies to improve operational efficiencies and solve real business problems. """
    
    model = T5ForConditionalGeneration.from_pretrained("t5-base", torchscript=True)
    tokenizer = T5Tokenizer.from_pretrained("t5-base", torchscript=True)
    inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=512, truncation=True)
    with torch.no_grad():
        traced_model = torch.jit.trace(model, inputs)
 
    torch.jit.save(traced_model, "traced_bert_summary.pt")

def load_bert():
    model_file = 'traced_bert_summary.pt'

    with open(model_file, 'rb') as f:
        model = f.read()
    startup_nodes = [{"host": "127.0.0.1", "port": "30001"}, {"host": "127.0.0.1", "port":"30002"}, {"host":"127.0.0.1", "port":"30003"}]
    cc = ClusterClient(startup_nodes = startup_nodes)
    hash_tags = cc.execute_command("RG.PYEXECUTE",  "gb = GB('ShardsIDReader').map(lambda x:hashtag()).run()")[0]
    print(hash_tags)
    for hash_tag in hash_tags:
        print("Loading model bert-summary{%s}" %hash_tag.decode('utf-8'))
        cc.modelset('bert-summary{%s}' %hash_tag.decode('utf-8'), 'TORCH', 'CPU', model)
        print(cc.infoget('bert-summary{%s}' %hash_tag.decode('utf-8')))

def redis_predict():
    tokenizer = AutoTokenizer.from_pretrained("t5-small")

    startup_nodes = [{"host": "127.0.0.1", "port": "30001"}, {"host": "127.0.0.1", "port":"30002"}, {"host":"127.0.0.1", "port":"30003"}]
    r = ClusterClient(startup_nodes = startup_nodes)
    hash_tags = r.execute_command("RG.PYEXECUTE",  "gb = GB('ShardsIDReader').map(lambda x:hashtag()).run()")[0]
    print(hash_tags)
    text = """At a very high level, one of the most critical steps in any ML pipeline is called AI serving, a task usually performed by an AI inference engine. The AI inference engine is responsible for the model deployment and performance monitoring steps in the figure above, and represents a whole new world that will eventually determine whether applications can use AI technologies to improve operational efficiencies and solve real business problems. """

     
    for hash_tag in hash_tags:
        
        inputs = tokenizer.encode_plus(text, max_length=512, add_special_tokens=True, return_tensors="np")
        input_ids = inputs['input_ids'].astype(np.int16)

        r.tensorset('input_ids{%s}' %hash_tag.decode('utf-8'), input_ids)

        r.modelrun('bert-summary{%s}' %hash_tag.decode('utf-8'), ['input_ids{%s}' %hash_tag.decode('utf-8'), 'attention_mask{%s}' %hash_tag.decode('utf-8'), 'token_type_ids{%s}' %hash_tag.decode('utf-8')])
        #                     



def main():
    # export_bert()
    # load_bert()
    redis_predict()
if __name__ == "__main__":
    main()
