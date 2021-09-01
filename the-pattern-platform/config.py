#!/usr/bin/python
from configparser import ConfigParser
from pathlib import Path
 
def config(filename='./conf/database.ini', section='redis'):
    # create a parser
    parser = ConfigParser()
    # read config file
    filepathname=Path(filename).resolve()
    parser.read(filepathname)

    # get section, default to redis
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
 
    return db