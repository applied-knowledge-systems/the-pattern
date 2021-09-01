import sys
from datetime import datetime
from pathlib import Path
LOG_PATH = Path('./logs/')
LOG_PATH.mkdir(exist_ok=True)

import logging
run_start_time = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
#FIXME: make a task name "Matching entities" dynamic
logfile = str(LOG_PATH/'log-{}-{}.txt'.format(run_start_time, "Matching entities"))

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