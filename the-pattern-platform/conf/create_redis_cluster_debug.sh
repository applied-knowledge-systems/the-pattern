#!/bin/bash
#------------ bootstrap the cluster nodes --------------------

CLUSTER_HOST=127.0.0.1
PORT=30000
TIMEOUT=2000
NODES=6
REPLICAS=1
PROTECTED_MODE=yes
ADDITIONAL_OPTIONS=""

# FIXME: docker command should be docker run -d -v \
# $PWD/cluster-config.conf:/usr/local/etc/redis/redis.conf \
# --name redis-1 --net red_cluster \
# redis redis-server /usr/local/etc/redis/redis.conf

if [ -a config.sh ]
then
    source "config.sh"
fi

# Computed vars
ENDPORT=$((PORT+NODES))

start_cmd="redis-server --port 6379 --protected-mode $PROTECTED_MODE --cluster-enabled yes --cluster-config-file nodes-${PORT}.conf --cluster-node-timeout $TIMEOUT --appendonly yes --appendfilename appendonly-${PORT}.aof --dbfilename dump-${PORT}.rdb --logfile ${PORT}.log --daemonize yes ${ADDITIONAL_OPTIONS}"
redis_image='redis:5.0-rc'
network_name='redis_cluster_net'

if [ "$1" == "start" ]
then
    while [ $((PORT < ENDPORT)) != "0" ]; do
        PORT=$((PORT+1))
        echo "Starting $PORT"
        echo $start_cmd
    done
    exit 0
fi

