#!/usr/bin/env bash
# this is a wrapper to bootstrap benchmark
./start.sh 
sudo apt install python3.9-venv
python3 -m venv ./venv_the_pattern
source ./venv_the_pattern/bin/activate
cd the-pattern-platform && pip3 install -r requirements.txt
pip3 install gears-cli==1.1.3 
./cluster_pipeline.sh
cd ../the-pattern-api/qasearch/ 
sh start_benchmark.sh 
