tokenizer = None 
    
import numpy as np
# import torch
import os 

config_switch=os.getenv('DOCKER', 'local')
if config_switch=='local':
    startup_nodes = [{"host": "127.0.0.1", "port": "30001"}, {"host": "127.0.0.1", "port":"30002"}, {"host":"127.0.0.1", "port":"30003"}]
else:
    startup_nodes = [{"host": "rgcluster", "port": "30001"}, {"host": "rgcluster", "port":"30002"}, {"host":"rgcluster", "port":"30003"}]

try: 
    from rediscluster import RedisCluster
    redisai_cluster_client = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)
except:
    print("Redis Cluster is not available")


def qa(question, sentence_key,hash_tag):
    ### question 
    ### use pre-computed context/answer text tensor populated by tokeniser_gears_redisai.py (run it first) 
    ### It's a new version using async/away and keymiss event
    ### get "bertqa{06S}_PMC7167827.xml:{06S}:11_When wheezing were recorded?"
    query_key=f"bertqa{hash_tag}_{sentence_key}_{question}"
    print("Query key " + query_key)
    answer=redisai_cluster_client.get(query_key)
    return answer

if __name__ == "__main__":
    question="When wheezing were recorded?"
    print(qa(question,"PMC261870.xml:{06S}:11",'{06S}'))
