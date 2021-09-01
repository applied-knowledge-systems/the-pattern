

- [ ]  start cluster using docker `./lauch_cluster_docker.sh` from the-pattern-platform/conf  
- [ ]  check loaded modules `redis-cli -c -p 30001 -h 127.0.0.1 INFO MODULES`
- [ ]  register pipeline `./cluster_pipeline.sh` from the-pattern-platform
- [ ]  check graph edges populated 
	- [ ]  `redis-cli -p 9001 -h 127.0.0.1 GRAPH.QUERY cord19medical "MATCH (e:entity)-[r]->(t:entity) RETURN count(r) as edge_count"`
	- [ ]  check graph nodes
		- [ ]  `redis-cli -p 9001 -h 127.0.0.1 GRAPH.QUERY cord19medical "MATCH (n:entity) RETURN count(n) as entity_count"` 
		- [ ]  Load bert models into redis AI
		- [ ]  Create API using graph search 
		- [ ]  validate API `curl -H "Content-Type: application/json" -X POST -d '{"search":"Effectiveness of community contact reduction"}' http://localhost:8181/qasearch |  jq .results`
```
  {
    "answer": "this would need tight coordination",
    "sentence": "This would need tight coordination among pharmaceutical companies, governments, regulatory agencies, and the World Health Organization (WHO), as well as novel and out-of-the-box approaches to cGMP production, release processes, regulatory science, and clinical trial design.",
    "sentencekey": "sentences:0020ab317ef923b740c1d3db52083a4e48495f8a:193:{1x3}",
    "title": "Perspective SARS-CoV-2 Vaccines: Status Report"
  }
```

## TODO 

- [X] Pre-compute content_text for content_text




# Pre-Compute tensors ("answer part")

```
gears-cli run --host 127.0.0.1 --port 30001 tokeniser_gears_redisai.py --requirements requirements.txt
```



# References:

BERT models require pair of sequences: [CLS] A [SEP] B [SEP] , see build_inputs_with_special_tokens from tokenizers and this [blog post](https://mccormickml.com/2020/03/10/question-answering-with-a-fine-tuned-BERT/)


New branch quickstart:
gears-cli run --host 127.0.0.1 --port 30001 tokeniser_gears_redisai.py --requirements requirements.txt 