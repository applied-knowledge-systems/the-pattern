# Quickstart:

1. Checkout https://github.com/applied-knowledge-systems/the-pattern-platform 
2. Launch [Launch Cluster Demo](https://github.com/applied-knowledge-systems/the-pattern-platform/blob/main/conf/launch_cluster_docker_demo.sh)
3. Create virtualenv & populate RedisGears cluster by running 'sh cluster_pipeline.sh'
4. Checkout API with BERT QA models: https://github.com/applied-knowledge-systems/the-pattern-api/tree/qa_bert_geared
5. Load models into each shard `cd /the-pattern-api/qasearch && python export_load_bert.py`
6. Pre-compute tensors `gears-cli run --host 127.0.0.1 --port 30001 tokeniser_gears_redisai.py --requirements requirements.txt`
7. Register trigger function `gears-cli run --host 127.0.0.1 --port 30001 qa_redisai_gear_map.py` 
8. Validate trigger function works:
```python
startup_nodes = [{"host": "127.0.0.1", "port": "30001"}, {"host": "127.0.0.1", "port":"30002"}, {"host":"127.0.0.1", "port":"30003"}]
from redisai import ClusterClient
redisai_cluster_client = ClusterClient(startup_nodes=startup_nodes)
question="Effectiveness of community contact reduction"
sentence_key="PMC261870.xml:{06S}:26"
slot = redisai_cluster_client.connection_pool.nodes.keyslot(sentence_key)
node = redisai_cluster_client.connection_pool.get_master_node_by_slot(slot)
connection = redisai_cluster_client.connection_pool.get_connection_by_node(node)
connection.send_command('RG.TRIGGER',"RunQABERT",sentence_key,question)
print(redisai_cluster_client.parse_response(connection,"RG.TRIGGER"))
```
shall return "effectiveness of community contact reduction", 
9. Register gears with keymiss event: 'gears-cli run --host 127.0.0.1 --port 30001 qa_redisai_gear_map_keymiss.py'
10. Run: redis-cli -c -p 30001 -h 127.0.0.1 get "cache{06S}{PMC261870.xml:{06S}:26}_Laser Correction" 



# References:

BERT models require pair of sequences: [CLS] A [SEP] B [SEP] , see build_inputs_with_special_tokens from tokenizers and this [blog post](https://mccormickml.com/2020/03/10/question-answering-with-a-fine-tuned-BERT/)


New branch quickstart:
gears-cli run --host 127.0.0.1 --port 30001 tokeniser_gears_redisai.py --requirements requirements.txt 