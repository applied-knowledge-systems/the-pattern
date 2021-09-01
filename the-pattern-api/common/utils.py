import sys
from datetime import datetime
from pathlib import Path
LOG_PATH = Path('./logs/')
LOG_PATH.mkdir(exist_ok=True)

import logging
run_start_time = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
#FIXME: make a task name "Matching entities" dynamic
logfile = str(LOG_PATH/'log-{}-{}.txt'.format(run_start_time, "API tasks"))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
    datefmt='%m/%d/%Y %H:%M:%S',
    handlers=[
        logging.FileHandler(logfile),
        logging.StreamHandler(sys.stdout)
    ])

logger = logging.getLogger()
log=logger.info


def remove_prefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix):]

def quote_string(v):
    """
    RedisGraph strings must be quoted,
    quote_string wraps given v with quotes incase
    v is a string.
    """

    if isinstance(v, bytes):
        v = v.decode()
    elif not isinstance(v, str):
        return v
    if len(v) == 0:
        return '""'

    if v[0] != '"':
        v = '"' + v

    if v[-1] != '"':
        v = v + '"'

    return v


import datetime 
import random
def random_date(start_date_year,end_date_year):
    start_date = datetime.date(2020, 1, 1) 
    end_date = datetime.date(2020, 2, 1) 
    time_between_dates = end_date - start_date 
    days_between_dates = time_between_dates.days 
    random_number_of_days = random.randrange(days_between_dates) 
    random_date = start_date + datetime.timedelta(days=random_number_of_days) 
    return random_date

import time
class FuncTimer():
    def __init__(self):
        self.start = time.time()
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        end = time.time()
        runtime = end - self.start
        msg = 'The function took {time} seconds to complete'
        print(msg.format(time=runtime))