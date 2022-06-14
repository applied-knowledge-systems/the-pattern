#!/usr/bin/env bash
# this is a wrapper to bootstrap benchmark
./start.sh 
docker-compose -f docker-compose.dev.yml exec api bash /app/docker_pipeline.sh
docker-compose -f docker-compose.dev.yml exec api bash /app/qasearch/start_benchmark_docker.sh
