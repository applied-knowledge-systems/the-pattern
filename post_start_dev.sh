docker-compose -f docker-compose.dev.yml exec rgcluster /cluster/create-cluster call RG.CONFIGSET ExecutionMaxIdleTime 300000
docker-compose -f docker-compose.dev.yml exec rgcluster /cluster/create-cluster call CONFIG SET proto-max-bulk-len 2048mb
docker-compose -f docker-compose.dev.yml exec rgcluster /cluster/create-cluster call CONFIG SET list-compress-depth 1
docker-compose -f docker-compose.dev.yml exec rgcluster /cluster/create-cluster call CONFIG SET cluster-node-timeout 30000 
docker-compose -f docker-compose.dev.yml exec rgcluster /cluster/create-cluster call config set appendonly no
docker-compose -f docker-compose.dev.yml exec rgcluster /cluster/create-cluster call config set save ""
