rconn=None 

def enable_debug():
    debug=execute('GET','debug{%s}'% hashtag())
    if debug=='1':
        debug=True
    else:
        debug=False
    return debug

def connecttoRedis():
    import redis 
    redis_client=redis.Redis(host='redisgraph',port=6379,charset="utf-8", decode_responses=True)
    return redis_client

def OnRegisteredConnect():
    global rconn
    rconn=connecttoRedis()
    return rconn

def process_item(record):
    debug=enable_debug()
    global rconn
    if not rconn:
        rconn=connecttoRedis()
    source_id=record['value']['source']
    source_name=record['value']['source_name']
    destination_id=record['value']['destination']
    destination_name=record['value']['destination_name']
    year=record['value']['year']
    if debug:
        log(f"Edges to Graph got source {source_id} {source_name} and {destination_id} {destination_name} and {year}")
        log("""MERGE (source: entity { id: '%s', label :'entity', name: '%s'}) 
         ON CREATE SET source.rank=1
         ON MATCH SET source.rank=(source.rank+1)
         MERGE (destination: entity { id: '%s', label: 'entity', name: '%s' })
         ON CREATE SET destination.rank=1
         ON MATCH SET destination.rank=(destination.rank+1)
         MERGE (source)-[r:related]->(destination)
         ON CREATE SET r.rank=1, r.year=%s
         ON MATCH SET r.rank=(r.rank+1)
         ON CREATE SET r.rank=1
         ON MATCH SET r.rank=(r.rank+1)""" % (source_id ,source_name,destination_id,destination_name,year))
    response=rconn.execute_command("GRAPH.QUERY", "cord19medical","""MERGE (source: entity { id: '%s', label :'entity', name: '%s'}) 
         ON CREATE SET source.rank=1
         ON MATCH SET source.rank=(source.rank+1)
         MERGE (destination: entity { id: '%s', label: 'entity', name: '%s' })
         ON CREATE SET destination.rank=1
         ON MATCH SET destination.rank=(destination.rank+1)
         MERGE (source)-[r:related]->(destination)
         ON CREATE SET r.rank=1, r.year=%s
         ON MATCH SET r.rank=(r.rank+1)
         ON CREATE SET r.rank=1
         ON MATCH SET r.rank=(r.rank+1)""" % (source_id ,source_name,destination_id,destination_name,year))
    if debug:
        log('Edges to graph finished with response '+" ".join(map(str,response)))


bg = GearsBuilder('StreamReader')
bg.foreach(process_item)
bg.register('edges_matched*', batch=1, mode="async_local",onRegistered=OnRegisteredConnect, onFailedPolicy='continue', trimStream=True)
