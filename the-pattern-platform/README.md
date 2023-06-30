# the-pattern-platform

This is a NLP pipeline based on RedisGears, this is evolution of  [Cord19Project](https://github.com/AlexMikhalev/cord19redisknowledgegraph)

The purpose of this part is NLP pipeline to turn text into knowledge graph ("it's about things, not strings") by matching text (terms) to Medical Methathesaurus UMLS (concepts).  As input this pipeline is using CORD19 competition Kaggle dataset - medical articles.

# Super Quick start using Docker

```
git checkout main
cd conf && launch_cluster_docker.sh
```

It will create docker network build and run Redisgraph and Rgcluster in two separate dockers.
In another terminal run
```
pip install gears-cli
sh cluster_pipeline.sh
```

It will populate all steps, submit 25 articles into cluster for processing and run matcher. There are few sleep statements to allow cluster to recover.

Check that Redis Graph instances were populated:

```
redis-cli -p 9001 -h 127.0.0.1 GRAPH.QUERY cord19medical "MATCH (n:entity) RETURN count(n) as entity_count"
```

# Architecture

Uses RedisGears using KeyReader, StreamReader

NLP Steps:

* Identify language [LangDetect](./lang_detect_gears_paragraphs.py) (It should be English)
* Split paragraphs into sentences using Spacy [spacy_sentences_streams.py](spacy_sentences_streams.py)
  * It can be done differently, but the point was to use large NLP library for processing
* Spellcheck sentences using [symspell_sentences_streamed.py](symspell_sentences_streamed.py)
* Match terms from sentences to UMLS concepts using pre-build Aho-Corasick Automata [sentences_matcher_streamed.py](sentences_matcher_streamed.py)
  * To build you own use aho_corasick_create_direct.py
    * You need to download and unpack umls-2019AB-metathesaurus.zip
* Populate Redis Graph [edges_to_graph_streamed.py](edges_to_graph_streamed.py)  from nodes (concepts) and edges (relationship between concepts, assumption is that if two concepts in the same sentence they are related). Redis Graph is separate instance listening on 9001.
* Run set_debug_key.py if you want to see logging on each step



# Quickstart

To run locally:

1. Compile RedisGears and Redis then use [conf/launch_cluster.sh](conf/launch_cluster.sh) to launch gears cluster, amend paths as needed

2. Start Redis Graph on port 9001 (or amend ports in conf/database.ini and in edges_to_graph_streamed.py)

3. Install gears-cli (pip install -r requirements.txt) and run sh cluster_pipeline_streams.sh to register functions

4. Populate cluster with sample of articles python RedisIntakeRedisClusterSample.py (Pass --nsamples n to increase size of the sample)

   1. Give a cluster kick using [lang_detect_gears_paragraphs_force.py](lang_detect_gears_paragraphs_force.py) if logs are not showing a lot of activity. Actual command will look like `gears-cli run --host 127.0.0.1 --port 30001 lang_detect_gears_paragraphs_force.py --requirements requirements_gears_lang.txt`

5. Validate Redis Graph is populated with `GRAPH.QUERY cord19medical "MATCH (n:entity) RETURN count(n) as entity_count"`



Alternatively, use Docker to launch RedisGears/Redis Graph, but pass commands from launch_cluster.sh via redis-cli -c

If you want to create you own NLP processing step lang_detect_gears_paragraphs_force.py is simplest example of KeyReader in batch mode, start with batch and then create a registration for events. StreamsReaders is probably closer to production, but pain in the back to debug.



# TODO

It's not ideal, most parts are hard coded, but I hope it's useful enough for NLP data scientists. Overall architecture is still as in [original](https://github.com/AlexMikhalev/cord19redisknowledgegraph)  project.

- [ ] Update the-pattern overall repository
- [x] Publish API server repository
- [x] Publish UI demo
- [ ] Publish demo BERT based QA
- [ ] Publish demo BERT based Summary
- [x] Create a docker deployment script for gears and Redis Graph
- [x] Add sentence splitter with https://github.com/mediacloud/sentence-splitter instead of spacy
- [x] Add redis cluster based debug flag (if execute('GET') then enable logs)

# Update 01.01.2021

New way to run most of the pipeline:
gears-cli run --host 127.0.0.1 --port 30001 gears_pipeline_sentence.py --requirements requirements_gears_pipeline.txt