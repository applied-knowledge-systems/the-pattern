# the-pattern
Overall repository for NLP pipeline, API and UI, design and architecture

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
