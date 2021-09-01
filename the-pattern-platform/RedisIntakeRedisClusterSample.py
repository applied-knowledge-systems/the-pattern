
import ujson as json
from redis.exceptions import ResponseError
from rediscluster import RedisCluster

import sys
from datetime import datetime
from pathlib import Path
LOG_PATH = Path('./logs/')
LOG_PATH.mkdir(exist_ok=True)

import logging
run_start_time = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
logfile = str(LOG_PATH/'log-{}-{}.txt'.format(run_start_time, "Parsing articles - sampled at 200"))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
    datefmt='%m/%d/%Y %H:%M:%S',
    handlers=[
        logging.FileHandler(logfile),
        logging.StreamHandler(sys.stdout)
    ])

logger = logging.getLogger()



import config
rc_list=json.loads(config.config(section='rediscluster')['rediscluster'])


rediscluster_client = RedisCluster(startup_nodes=rc_list, decode_responses=True)

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
n_cpus = os.cpu_count()
logger.info(f'Number of CPUs: {n_cpus}')
executor = ThreadPoolExecutor(max_workers=n_cpus)

cwd=Path.cwd()
datapath=cwd.joinpath('./data/')
print(datapath)

import argparse
parser = argparse.ArgumentParser(description='This is a Intake python program')
parser.add_argument('--nsamples', type=int, default=10)
parser.add_argument('--path', type=str, default=".")

def parse_json_body_text(json_filename):
    logger.info("Processing .." + json_filename.stem)
    with open(json_filename) as json_data:
        data = json.load(json_data)
        for body_text in data['body_text']:
            para = body_text['text']
            yield para

#process document return sentences and entities 
def process_file(f, rediscluster_client=rediscluster_client):
    article_id=f.stem
    logger.info("Processing article_id "+ article_id)
    if rediscluster_client.sismember('processed_docs_stage1_para', article_id):
        logger.info("already processed "+ article_id)
        return article_id
    article_body=[]
    for para in parse_json_body_text(f):
        article_body.append(para)
    rediscluster_client.set(f"paragraphs:{article_id}"," ".join(article_body))
    rediscluster_client.sadd('processed_docs_stage1_para',article_id) 
    return article_id

# main submission loop
counter=0 
processed=[]
args = parser.parse_args()
json_filenames = datapath.glob(args.path+'/**/*.json')
for each_file in json_filenames:
    logger.info("Submitting task")
    task=executor.submit(process_file,each_file,rediscluster_client)
    processed.append(task)
    counter+=1
    if counter>args.nsamples:
        break

    
logger.info("Waiting for tasks to complete")
for each_task in as_completed(processed):
    logger.info(task.result())
logger.info("Completed")




