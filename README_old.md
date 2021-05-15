# the-pattern
Overall repository for CORD19 medical NLP pipeline, API and UI, design and architecture. 
Demo: http://thepattern.digital/

# The challenge 

The medical profession put a lot of effort into collaboration, starting from Latin as a common language to industry-wide thesauruses like [UMLS](https://www.nlm.nih.gov/research/umls/index.html). Yet if full of scandals where publication in the prestigious journal would be retracted and the World Health Organisation would change its policy advice based on the article. It's not uncommon to see conversations like this where bits of randomness were presented as major findings. I think "paper claiming that eating a bat-like Pokémon sparked the spread of COVID-19" takes a prize. One would say that editors in those journals don't do their job, and while it may seem true, I would say they had no chance: with a number of publications about COVID (SARS-V) passing 300+ per day, we need better tools to navigate via such flow of information.
 
When I am exploring topics on science or engineering, I look at the diversity of the opinion, not the variety of the same cluster of words, same thought. I want to avoid confirmation bias. I want to find articles relevant to the same concept, not necessarily the ones which have similar words. My focus is to build a natural language processing pipeline, capable of handling a large number of documents and concepts, incorporating System 1 AI (fast, intuitive reasoning) and System 2 (high-level reasoning) and then present knowledge in a modern VR/AR visualisation. Search or rather information exploration should be spatial preferably in VR (memory palace, see Theatre of Giulio Camillo). A force-directed graph is a path towards it, where visuals are assisted by text — relevant text pops up on the connection and where people explore the concepts and then dig deeper into text. The purpose of the pipeline that knowledge should be re-usable and shareable.

# Why use RedisGears for data scientists?

RedisGears have enormous potential, particularly for text processing - you can process your data “on data” without need to move them in and out of memory, summary of the important points:
1.In Memory storage (Horizontally scalable if it’s Redis cluster)
2.Processing of data (on data) without need to move in and out
3.Gears - like Spark on Hadoop, process data intelligently on storage(in-memory) without need to move data in and out
4.Redis in cluster mode with RedisGears and python enabled takes 20 MB RAM. Think how much more data you can shuffle into your laptop or server.


# Why The Pattern name
The name is from [Roger Zelazny "The Chronicles of Amber"](https://en.wikipedia.org/wiki/The_Chronicles_of_Amber#The_Pattern_and_the_Logrus) where The Pattern is the foundation of the universe of order. 
I believe in the modern world we need new tools to fight the chaos of the information, particularly for such important issues as medical research and literature. 

# Quickstart for development

## Pre-requisite

Ensure that you install virtualenv in your system

```
brew install pyenv-virtualenv  
```

## Cloning the Repository


```
git clone --recurse-submodules https://github.com/applied-knowledge-systems/the-pattern.git
cd the-pattern
docker-compose -f docker-compose.dev.yml up --build -d
bash post_start_dev.sh
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

Production compose file pinned to a dedicated server and only differs by IP and paths

# Documentation
Still relevant [one](https://alexmikhalev.github.io/cord19redisknowledgegraph/)
The journey in [blog](https://alexmikhalev.medium.com)
