# The Pattern: Machine Learning Natural Language Processing meets VR/AR 
## Short description
To fight ever-increasing complexity, "The Pattern" projects help find relevant knowledge using Artificial Intelligence and novel UX elements, all powered by Redis - new generation real time data fabric turned into knowledge fabric

Overall repository for CORD19 medical NLP pipeline, API and UI, design and architecture.

Demo: http://thepattern.digital/

# The challenge 

The medical profession put a lot of effort into collaboration, starting from Latin as a common language to industry-wide thesauruses like [UMLS](https://www.nlm.nih.gov/research/umls/index.html). Yet if full of scandals where publication in the prestigious journal would be retracted and the World Health Organisation would change its policy advice based on the article. I think "paper claiming that eating a bat-like Pokémon sparked the spread of COVID-19" takes a prize. One would say that editors in those journals don't do their job, and while it may seem true, I would say they had no chance: with a number of publications about COVID (SARS-V) passing 300+ per day, we need better tools to navigate via such flow of information.
 
When I am exploring topics on science or engineering, I look at the diversity of the opinion, not the variety of the same cluster of words, same thought. I want to avoid confirmation bias. I want to find articles relevant to the same concept, not necessarily the ones which have similar words. My focus is to build a natural language processing pipeline, capable of handling a large number of documents and concepts, incorporating System 1 AI (fast, intuitive reasoning) and System 2 (high-level reasoning) and then present knowledge in a modern VR/AR visualisation. Search or rather information exploration should be spatial preferably in VR (memory palace, see Theatre of Giulio Camillo). A force-directed graph is a path towards it, where visuals are assisted by text — relevant text pops up on the connection and where people explore the concepts and then dig deeper into text. The purpose of the pipeline that knowledge should be re-usable and shareable.

# Quickstart for development

## Pre-requisite

Ensure that you install virtualenv in your system, docker and docker-compose (`apt install docker-compose`)

```
brew install pyenv-virtualenv  
```

## Start platform 

```
git clone --recurse-submodules https://github.com/applied-knowledge-systems/the-pattern.git
cd the-pattern
./start.sh
cd ./the-pattern-platform/
source ~/venv_cord19/bin/activate #or create new venv
pip install -r requirements.txt
bash cluster_pipeline.sh
```

Wait for a bit and then check:
1) Redis Graph populated: 

```
redis-cli -p 9001 -h 127.0.0.1 GRAPH.QUERY cord19medical "MATCH (n:entity) RETURN count(n) as entity_count" 
redis-cli -p 9001 -h 127.0.0.1 GRAPH.QUERY cord19medical "MATCH (e:entity)-[r]->(t:entity) RETURN count(r) as edge_count"
```

2) API responds: 

```
curl -i -H "Content-Type: application/json" -X POST -d '{"search":"How does temperature and humidity affect the transmission of 2019-nCoV"}' http://localhost:8080/gsearch
```
## Start UI 

```
cd the-pattern-ui
npm install 
npm install -g @angular/cli@9
ng serve
```

##  Question Answering API:
``
cd the-pattern-api/qasearch/
sh start.sh
```

WARNING: this will download and pre-load 1.4 GB BERT QA model on each shard. May crash on laptop.
Validate by running: 

```
curl -H "Content-Type: application/json" -X POST -d '{"search":"How does temperature and humidity affect the transmission of 2019-nCoV?"}' http://localhost:8080/qasearch
```

## Summarization pipeline 

Go to the repository on RedisGears cluster from main "the-pattern" repo:

```
cd the-pattern-bart-summary
# source same enviroment with gears-cli (no other dependencies required)
source ~/venv_cord19/bin/activate 
gears-cli run --host 127.0.0.1 --port 30001 tokenizer_gears_for_sum.py --requirements requirements.txt
```
This is a synchronious task, may time out but can be safely re-run (keeps track in RedisMod, idempotent operations)

On GPU enabled instance or server, configure NVidia drivers:

```bash 

    sudo apt update
    sudo apt install nvidia-340
    lspci | grep -i nvidia
    sudo apt-get install linux-headers-$(uname -r)
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID | sed -e 's/\.//g')
    wget https://developer.download.nvidia.com/compute/cuda/repos/$distribution/x86_64/cuda-$distribution.pin
    sudo mv cuda-$distribution.pin /etc/apt/preferences.d/cuda-repository-pin-600
    sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/$distribution/x86_64/7fa2af80.pub
    echo "deb http://developer.download.nvidia.com/compute/cuda/repos/$distribution/x86_64 /" | sudo tee /etc/apt/sources.list.d/cuda.list
    sudo apt-get update
    sudo apt-get -y install cuda-drivers
    # install anaconda
    curl -O https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh
    sh Anaconda3-2020.11-Linux-x86_64.sh
    source ~/.bashrc
    conda create -n thepattern_env python=3.8
    conda activate thepattern_env
    conda install pytorch==1.7.1 torchvision==0.8.2 torchaudio==0.7.2 cudatoolkit=11 -c pytorch

```

Configure access from instance to RedisGraph docker image (or use Redis Enterprise), I use zerotier to connect VMs together.

```
git clone https://github.com/applied-knowledge-systems/the-pattern-bart-summary.git
#start tmux 
conda activate thepattern_env
pip3 install -r requirements.txt
python3 summary_processor_t5.py
```

# Architecture Diagrams

## Overall flow

![Overall flow](https://github.com/applied-knowledge-systems/the-pattern/blob/main/docs/img/overall_flow.png "Overall Flow")

## NLP pipeline 1

![NLP Pipeline 1](https://github.com/applied-knowledge-systems/the-pattern/blob/main/docs/img/Pipeline1.png "NLP Pipeline 1") 

## NLP pipeline 2: BERT QA

![NLP Pipeline 2](https://github.com/applied-knowledge-systems/the-pattern/blob/main/docs/img/Pipeline2.png "NLP Pipeline 2") 

## NLP Pipeline 3: T5 for Summarization 

![NLP Pipeline 3](https://github.com/applied-knowledge-systems/the-pattern/blob/main/docs/img/Pipeline3.png "NLP Pipeline 3")  

# Screenshots

![Screenshot](https://github.com/applied-knowledge-systems/the-pattern/blob/main/docs/img/screenshot_one.png "Screenshot")  

![Screenshot2](https://github.com/applied-knowledge-systems/the-pattern/blob/main/docs/img/screenshot_two.png "Screenshot 2") 

![Screenshot3](https://github.com/applied-knowledge-systems/the-pattern/blob/main/docs/img/screenshot_three.png "Screenshot 3") 


# Most interesting RedisCommands
## In Pipeline 1

`the-pattern-platform/parse_publish_dates_threaded.py` - unzips and parses metadata.zip, where names of files, titles and years extracted into HASH:

```
    redis_client.hset(f"article_id:{article_id}",mapping={'title': each_line['title']})
    redis_client.hset(f"article_id:{article_id}",mapping={'publication_date':each_line['publish_time']})
```

`the-pattern-platform/RedisIntakeRedisClusterSample.py`  works by reading JSON files - samples in data/sample folder, parsing JSON into String:
`rediscluster_client.set(f"paragraphs:{article_id}"," ".join(article_body))`


`the-pattern-platform/gears_pipeline_sentence_register.py` - main pre-processing tasks using RedisGears, listens to updates on `paragraphs:` key:

```
gb = GB('KeysReader')
gb.filter(filter_language)
gb.flatmap(parse_paragraphs)
gb.map(spellcheck_sentences)
gb.foreach(save_sentences)
gb.count()
gb.register('paragraphs:*',keyTypes=['string','hash'], mode="async_local")
```
uses RedisGears and HSET/SADD.

### Turn Sentences into Edges (Sentence) and Nodes(things/Concepts) using Aho-Corasick algorithm

`the-pattern-platform/sentences_matcher_register.py`

```
bg = GearsBuilder('KeysReader')
bg.foreach(process_item)
bg.count()
bg.register('sentence:*',  mode="async_local",onRegistered=OnRegisteredAutomata)
```

Creates stream on each shard for next step using `'XADD', 'edges_matched_{%s}' % shard_id, '*','source',f'{source_entity_id}','destination',f'{destination_entity_id}','source_name',source_canonical_name,'destination_name',destination_canonical_name,'rank',1,'year',year)`

### Populate RedisGraph from RedisGears

`the-pattern-platform/edges_to_graph_streamed.py` works by creating nodes, edges in RedisGraph or updating their ranking:

```
"GRAPH.QUERY", "cord19medical","""MERGE (source: entity { id: '%s', label :'entity', name: '%s'}) 
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
```


### Querying RedisGraph data during API calls:

`the-pattern-api/graphsearch/graph_search.py`

Edges with years node ids, limits and years:

```
"""WITH $ids as ids MATCH (e:entity)-[r]->(t:entity) where (e.id in ids) and (r.year in $years) RETURN DISTINCT e.id, t.id, max(r.rank), r.year ORDER BY r.rank DESC LIMIT $limits"""
```


Nodes:

```
"""WITH $ids as ids MATCH (e:entity) where (e.id in ids) RETURN DISTINCT e.id,e.name,max(e.rank)"""
```


Populating article metadata 

```
redis_client.hset(f"article_id:{article_id}",mapping={'title': each_line['title']})
```
A lot of RedisGears code, main [file](./the-pattern-platform/gears_pipeline_sentence_register.py), SADD, SMEMBER, SREM.

### Most humorious code in pipeline:
```
    import httpimport
    with httpimport.remote_repo(['stop_words'], "https://raw.githubusercontent.com/explosion/spaCy/master/spacy/lang/en/"):
        import stop_words
    from stop_words import STOP_WORDS

    with httpimport.remote_repo(['utils'], "https://raw.githubusercontent.com/applied-knowledge-systems/the-pattern-automata/main/automata/"):
        import utils
    from utils import loadAutomata, find_matches
```
(show it to you security architect)

## In Pipeline 2 

Most advanced code is in `the-pattern-api/qasearch/qa_bert.py` querying RedisGears+RedisAI cluster given user's question: 

get "bertqa{5M5}_PMC140314.xml:{5M5}:44_When air samples collected?" 

this queries bertqa prefix on shard {5MP} where PMC140314.xml:{5M5}:44 is the key of pre-tokenised REDIS AI Tensor (potential answer) and "When air samples collected?" is the question from the user. Redis Gears captures keymiss event `the-pattern-api/qasearch/qa_redisai_gear_map_keymiss_np.py`:

```
gb = GB('KeysReader')
gb.map(qa_cached_keymiss)
gb.register(prefix='bertqa*', commands=['get'], eventTypes=['keymiss'], mode="async_local")
```

and runs redisAI.getTensorFromKey, redisAI.createModelRunner, redisAI.createTensorFromBlob, redisAI.modelRunnerAddInput, redisAI.modelRunnerRunAsync in async/await - non-blocking main thread mode, models pre-loaded on each shard using AI.modelset in `the-pattern-api/qasearch/export_load_bert.py`.

## In Pipeline 3

Summarisation works by running on `sentence:` prefix and running t5-base transformers tokenizer, saving results in RedisGraph using simple SET command and python.pickle module, adding summary key (derived from article_id) into `rconn.sadd('processed_docs_stage3_queue', summary_key)`.

`summary_processor_t5.py` subscribes to queue running simple SET and SREM commands and then updates hash in RedisGraph: `redis_client.hset(f"article_id:{article_id}",mapping={'summary': output})`


# Deploy

The Pattern platform using latest (bleeding edge) RedisGears and RedisAI features, best way to deploy and use docker compose provided. 
RedisGraph docker is using standard redismod docker image and can be deployed on RedisEnterprise.

### Google Cloud Run

[![Run on Google
Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run/?git_repo=https://github.com/applied-knowledge-systems/the-pattern-platform)

### Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)


# Why use RedisGears for data scientists?

RedisGears have enormous potential, particularly for text processing - you can process your data “on data” without need to move them in and out of memory, summary of the important points:
1.In Memory storage (Horizontally scalable if it’s Redis cluster)
2.Processing of data (on data) without need to move in and out
3.Gears - like Spark on Hadoop, process data intelligently on storage(in-memory) without need to move data in and out
4.Redis in cluster mode with RedisGears and python enabled takes 20 MB RAM. Think how much more data you can shuffle into your laptop or server.


# Why The Pattern name
The name is from [Roger Zelazny "The Chronicles of Amber"](https://en.wikipedia.org/wiki/The_Chronicles_of_Amber#The_Pattern_and_the_Logrus) where The Pattern is the foundation of the universe of order.  
I believe in the modern world we need new tools to fight the chaos of the information, particularly for such important issues as medical research and literature. 


# Documentation
Still relevant [one](https://alexmikhalev.github.io/cord19redisknowledgegraph/)
The journey in [blog](https://alexmikhalev.medium.com)




