git clone --depth 1 --recursive https://github.com/RedisGears/RedisGears.git
cd RedisGears
git submodule update --init --recursive 
cd .. 
docker-compose -f docker-compose.debs.yml build