# the-pattern-api
API gateway for The Pattern

This is a front end API to data pipeline, to have a right contenct in Redis/Redis Graph:

* Launch RedisGears pipeline via launch docker cluster or better via docker compose
* Register RedisGears functions
* Add metadata parse_publish_dates.py
* python RedisIntakeRedisClusterSample.py --nsamples 105 --path cord19-research-challenge
* gears-cli run --host 127.0.0.1 --port 30001 sentences_matcher_gears.py  --requirements requirements_gears_aho.txt
# Quickstart

assuming you have Redis Graph on localhost 9001
```
./start.sh
```


validate

```
curl -i -H "Content-Type: application/json" -X POST -d '{"search":"laser correction operation"}' http://127.0.0.1:8080/search
Access-Control-Allow-Origin: *
Server: Werkzeug/1.0.1 Python/3.8.5
Date: Thu, 31 Dec 2020 06:30:39 GMT

{"search_result":{"links":[{"source":"C5162902","target":"C5141303"},{"source":"C5162902","target":"C5191700"},{"source":"C5141303","target":"C5191700"}],"nodes":[{"id":"C5162902","name":"C5162902"},{"id":"C5141303","name":"C5141303"},{"id":"C5191700","name":"C5191700"}]}}
```

```
curl -X GET "http://127.0.0.1:8080/edge/edges:C5191700:C5125137"
{
  "results": [
    {
      "sentence": "In accordance with the latter observation equine arteritis virus RNA transcribed in nitro from full length cD A templates is infectious only when provided with a cap Glaser it al 1999",
      "sentencekey": "sentence:PMC136939.xml:{0cY}:45",
      "title": "Discontinuous and non-discontinuous subgenomic RNA transcription in a nidovirus"
    }
  ],
  "years": [
    "2002"
  ]
}
```
BERT Question/Answering

```
curl -H "Content-Type: application/json" -X POST -d '{"search":"Effectiveness of community contact reduction"}' http://127.0.0.1:8080/qasearch | jq .results
```

Register on Redis Enterprise and pass REDIS_ENDPOINT_URI and REDIS_PASSWORD

### Google Cloud Run

[![Run on Google
Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run/?git_repo=https://github.com/applied-knowledge-systems/the-pattern-api.git)

### Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/applied-knowledge-systems/the-pattern-api.git)
