
import ujson as json
from redis.exceptions import ResponseError

try:
    import redis
    import config
    redis_client = redis.Redis(host=config.config()['host'],port=config.config()['port'],charset="utf-8", decode_responses=True)
except:
    log("Redis is not available ")


from common.utils import *

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
# n_cpus = os.cpu_count()
# FIXME: multithreading can be safely removed in favour of redis_client.pipeline, Redis is a single thread write
n_cpus = 1
logger.info(f'Number of CPUs: {n_cpus}')
executor = ThreadPoolExecutor(max_workers=n_cpus)

from pathlib import Path

#path to cord19 dataset 
#FIXME: make a separate config for paths
datapath = Path('../the-pattern/data/CORD-19-research-challenge/')

setname='processed_docs_stage1_title'

def parse_json_title(json_filename):
    with open(json_filename) as json_data:
        data = json.load(json_data)
        return str(data['metadata']['title'])

#process document return sentences and entities 
def process_file(f, redis_client=redis_client):
    article_id=f.stem
    logger.info(f"Processing article_id {article_id}" )
    if redis_client.sismember(setname, article_id):
        logger.info(f"already processed {article_id}")
        return article_id
    article_title=parse_json_title(f)
    redis_client.hset(f"article_id:{article_id}",mapping={'title':article_title})
    redis_client.sadd(setname,article_id) 
    return article_id

# main submission loop 
processed=[]
counter=0
start_time=datetime.now()
json_filenames = datapath.glob('**/*.json')
for each_file in json_filenames:
    logger.info("Submitting task")
    task=executor.submit(process_file,each_file,redis_client)
    processed.append(task)


    
logger.info("Waiting for tasks to complete")
for each_task in as_completed(processed):
    logger.info(task.result())
logger.info("Completed in: {:s}".format(str(datetime.now()-start_time)))



