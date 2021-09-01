from redis.exceptions import ResponseError
from common.utils import *

"""
This rather humourious script attaches metadata to files, 
the only reliable way to do it with CORD19 metadata is with filename,
which on occasions equal file SHA or filename. 
Overall it's rather suboptimal solution, for faster processing use async or redis-cli --pipe 

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

with redis_client.pipeline() as pipe:
    with ZipFile('./data/metadata.zip') as zf:
            with zf.open('metadata.csv', 'r') as infile:
                reader = csv.DictReader(TextIOWrapper(infile, 'utf-8'))
                for each_line in reader:
                    filelist = [x.strip() for x in each_line['pdf_json_files'].split(";")]
                    for filename in filelist:
                        record_to_redis(redis_client, each_line,filename)
                    filelist = [x.strip() for x in each_line['pmc_json_files'].split(";")]
                    for filename in filelist:
                        record_to_redis(redis_client, each_line,filename)
pipe.execute()
print("Saving data")
redis_client.bgsave()