#!/usr/bin/env bash
# this is a wrapper to bootstrap benchmark
./start.sh 
docker-compose -f docker-compose.dev.yml exec api bash /app/docker_pipeline.sh
sleep 10
docker-compose -f docker-compose.dev.yml exec api bash /app/start_qa_docker.sh
