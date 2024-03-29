rm -rf RedisGears
git clone --branch v1.2.4 --depth 1 --recursive https://github.com/RedisGears/RedisGears.git
cd RedisGears
git submodule update --init --recursive 
cd .. 
docker-compose -f docker-compose.debs.yml build
docker push ghcr.io/applied-knowledge-systems/rgcluster:edge
