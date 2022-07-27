#!/usr/bin/env bash
# this is a wrapper to bootstrap pipeline
./start.sh 
docker-compose -f docker-compose.dev.yml exec api bash /app/docker_pipeline.sh
