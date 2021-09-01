#!flask/bin/python
from flask import Flask, jsonify, request,abort
from flask_cors import CORS, cross_origin
app = Flask(__name__)
app.config['SECRET_KEY']='P3JqafOaPHmi7DV96aZA'
app.config.update(dict(
  PREFERRED_URL_SCHEME = 'https'
))

CORS(app,supports_credentials=True)

import httpimport
with httpimport.remote_repo(['utils'], "https://raw.githubusercontent.com/applied-knowledge-systems/the-pattern-automata/main/automata/"):
    import utils
from utils import loadAutomata, find_matches

from common.utils import *

import os 

config_switch=os.getenv('DOCKER', 'local')
REDISGRAPH_PORT=os.getenv('REDISGRAPH_PORT', "9001")
if config_switch=='local':
    startup_nodes = [{"host": "127.0.0.1", "port": "30001"}, {"host": "127.0.0.1", "port":"30002"}, {"host":"127.0.0.1", "port":"30003"}]
    host="127.0.0.1"
    port=REDISGRAPH_PORT
else:
    startup_nodes = [{"host": "rgcluster", "port": "30001"}, {"host": "rgcluster", "port":"30002"}, {"host":"rgcluster", "port":"30003"}]
    host="redisgraph"
    port=REDISGRAPH_PORT

try:
    import redis
    redis_client = redis.Redis(host=host,port=port,charset="utf-8", decode_responses=True)
except:
    log("Redis is not available ")

try: 
    from rediscluster import RedisCluster
    rediscluster_client = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)
except:
    log("RedisCluster is not available")

from graphsearch.graph_search import * 

from flask import session, redirect, url_for
from functools import wraps

def redirect_url(default='index'):
    return request.args.get('next') or \
           request.referrer or \
           request.url

@app.route('/index')
def index():
    return "Nothing here"

# def login_required(function_to_protect):
#     @wraps(function_to_protect)
#     def wrapper(*args, **kwargs):
#         user_id = session.get('user_id')
#         print("Did we get user_id from session? " + str(user_id))
#         print(f"Referer {request.referrer}")
#         print(f"Request URL {request.url}")
#         if user_id:
#             user_id=redis_client.hget("user:%s" % user_id,'id')
#             if user_id:
#                 # Success!
#                 return function_to_protect(*args, **kwargs)
#             else:
#                 print("Session exists, but user does not exist (anymore)")
#                 response=redirect(url_for('login'))
#                 return response
#         else:
#             print("Please log in")
#             response=redirect(url_for('login',next=redirect_url()))
#             return response
#     return wrapper

@app.route('/login')
def login():
    user_id = session.get('user_id')
    if not user_id:
        new_user=redis_client.incr("user_id_counter")
        print(new_user)
        redis_client.hset("user:%s" % new_user,mapping={'id': new_user})
        session['user_id']=new_user
        if 'url' in session:
            response=redirect(session['url'])
            response.set_cookie('user_id', str(new_user))
            return response
        else:
            response=redirect(redirect_url())
            response.set_cookie('user_id', str(new_user))
            return response

@app.route('/edge/<edge_string>')
def get_edgeinfo(edge_string):
    """
    Tested with edges:C5162902:C5190121
    """
    log("Edge string "+edge_string)
    years_set=set()
    edges_query=remove_prefix(edge_string,'edges:')
    result_table=[]
    unique_id=set()
    edge_scored=redis_client.zrangebyscore(f"edges_scored:{edges_query}",'-inf','inf',0,5)
    if edge_scored:
        for sentence_key in edge_scored:
            *head,tail=sentence_key.split(':')
            sentence=rediscluster_client.hget(":".join(head),tail)
            article_id=head[1]
            if article_id not in unique_id:
                unique_id.add(article_id)
            else:
                continue    
            title=redis_client.hget(f"article_id:{article_id}",'title')
            year_fetched=redis_client.hget(f"article_id:{article_id}",'year')
            summary_fetched=redis_client.hget(f"article_id:{article_id}",'summary')
            if year_fetched:
                years_set.add(year_fetched)
            if not summary_fetched:
                redis_client.sadd("failed_summary",f"article_id:{article_id}")
                summary_fetched="TBC"

            result_table.append({'title':title,'sentence':str(sentence),'sentencekey':sentence_key,'summary':summary_fetched,'article_id':f"article_id:{article_id}"})
    else:
        result_table.append(redis_client.hgetall(f'{edge_string}'))
    
    print(years_set)
    return jsonify({'results': result_table,'years':list(years_set)}), 200

@app.route('/exclude', methods=['POST','GET'])
def mark_node():
    if request.method == 'POST':
        print(request.json)
        if 'id' in request.json:
            node_id=request.json['id']
    else:
        print(request.args)
        if 'id' in request.args:
            node_id=request.args.get('id')
    user_id = session.get('user_id')
    log(f"Got user {user_id} from session")
    if not user_id:
        user_id = request.cookies.get('user_id')
        log(f"Got user {user_id} from cookie")
    redis_client.sadd("user:%s:mnodes" % user_id,node_id)
    response = jsonify(message=f"Finished {node_id} and {user_id}")
    return response


@app.route('/search', methods=['POST','GET'])
def gsearch_task():
    """
    this search using Redis Graph to get list of nodes and links
    """
    years_query=None
    limit=300
    user_id = session.get('user_id')
    log(f"Got user {user_id} from session")
    if not user_id:
        user_id = request.cookies.get('user_id')
        log(f"Got user {user_id} from cookie")
        if not user_id: 
            """ create new user """ 
            new_user=redis_client.incr("user_id_counter")
            redis_client.hset("user:%s" % new_user,mapping={'id': new_user})
            session['user_id']=new_user
            user_id=new_user

    if request.method == 'POST':
        if not 'search' in request.json:
            abort(400)
        else:
            search_string=request.json['search']

        if 'years' in request.json:
            print("Years arrived")
            years_query=request.json['years']
            print(years_query)
            years_query=[int(x) for x in years_query]
            

        if 'limit' in request.json:
            limit=request.json['limit']
            print("Limit arrived",limit)
    else:
        if not bool(request.args.get('q')):
            abort(400)
        else:
            search_string=request.args.get('q')
            if request.args.get('limit'):
                limit=request.args.get('limit')
                print("Limit arrived via get", limit)
            
    user_id = session.get('user_id')
    if user_id:
        print(f"Got user id {user_id}")
        mnodes=redis_client.smembers("user:%s:mnodes" % user_id)
    else:
        mnodes=set()
    nodes=match_nodes(search_string)    
    links, nodes, years_list = get_edges(nodes,years_query,limit,mnodes)
    node_list=get_nodes(nodes)
    response = jsonify({'nodes': node_list,'links': links,'years':years_list})
    if not request.cookies.get('user_id'):
        print("User id" +str(user_id))
        response.set_cookie('user_id',str(user_id))
    return response

from qasearch.qa_bert import *
@app.route('/qasearch', methods=['POST'])
def qasearch_task():
    """
    this search using Redis Graph to get list of articles and sentences and then calls BERT QA model to create answer
    TODO: pre-process articles with qa tokeniser 
    """
     

    if not request.json or not 'search' in request.json:
        abort(400)
    question=request.json['search']
    nodes=match_nodes(question)
    links,_,_=get_edges(nodes,limits=1)
    result_table=[]
    for each_record in links[0:5]:  
        edge_query=each_record['source']+":"+each_record['target'] 
        print(edge_query)
        edge_scored=redis_client.zrangebyscore(f"edges_scored:{edge_query}",'-inf','inf',0,5)
        if edge_scored:
            for sentence_key in edge_scored:
                *head,tail=sentence_key.split(':')
                sentence=rediscluster_client.hget(":".join(head),tail)
                article_id=head[1]
                title=redis_client.hget(f"article_id:{article_id}",'title')
                hash_tag=head[-1]
                answer=qa(question,remove_prefix(sentence_key,'sentence:'),hash_tag)
            result_table.append({'title':title,'sentence':sentence,'sentencekey':sentence_key,'answer':answer})        

    return jsonify({'links': links,'results':result_table}), 200


if __name__ == "__main__":
    app.run(port=8181, host='0.0.0.0',debug=True)

