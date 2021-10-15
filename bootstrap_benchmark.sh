# this is a wrapper to bootstrap benchmark
./start.sh 
apt install python3.9-venv
python3 -m venv ./venv_the_pattern
source ./venv_the_pattern/bin/activate
cd the-pattern-platform && pip install -r requirements.txt
pip install gears-cli 
./cluster_pipeline.sh
cd ../the-pattern-api/qasearch/ 
sh start.sh