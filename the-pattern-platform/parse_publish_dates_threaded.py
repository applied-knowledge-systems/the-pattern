from redis.exceptions import ResponseError
from common.utils import *

"""
This rather humourious script attaches metadata to files, 
the only reliable way to do it with CORD19 metadata is with filename,
which on occasions equal file SHA or filename. 
For faster processing use async or redis-cli --pipe 

"""

try:
    import redis
    import config
    redis_client = redis.Redis(host=config.config(section='redis_local')['host'],port=config.config(section='redis_local')['port'],charset="utf-8", decode_responses=True)
except:
    log("Redis is not available ")

import csv
from io import TextIOWrapper
from zipfile import ZipFile

from pathlib import Path

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
n_cpus = os.cpu_count()
logger.info(f'Number of CPUs: {n_cpus}')
executor = ThreadPoolExecutor(max_workers=n_cpus)

def record_to_redis(redis_client, each_line,filename):
    article_id=Path(filename).stem
    redis_client.hset(f"article_id:{article_id}",mapping={'title': each_line['title']})
    redis_client.hset(f"article_id:{article_id}",mapping={'publication_date':each_line['publish_time']})
    date_list=each_line['publish_time'].split('-')
    if len(date_list) == 3:
        redis_client.hset(f"article_id:{article_id}",mapping={'year':date_list[0]})
        redis_client.hset(f"article_id:{article_id}",mapping={'month':date_list[1]})
        redis_client.hset(f"article_id:{article_id}",mapping={'day':date_list[2]})
    elif len(date_list) == 1:
        redis_client.hset(f"article_id:{article_id}",mapping={'year':date_list[0]})
    else:
        log(f"Incorrect date {date_list} in {article_id}")

processed=[]
with ZipFile('./data/metadata.zip') as zf:
        with zf.open('metadata.csv', 'r') as infile:
            reader = csv.DictReader(TextIOWrapper(infile, 'utf-8'))
            for each_line in reader:
                filelist = [x.strip() for x in each_line['pdf_json_files'].split(";")]
                for filename in filelist:
                    task=executor.submit(record_to_redis,redis_client,each_line,filename)
                    processed.append(task)
                filelist = [x.strip() for x in each_line['pmc_json_files'].split(";")]
                for filename in filelist:
                    task=executor.submit(record_to_redis,redis_client,each_line,filename)
                    processed.append(task)
print("End of metadata parsing")
logger.info("Waiting for tasks to complete")
for each_task in as_completed(processed):
    task.result()
logger.info("Completed")