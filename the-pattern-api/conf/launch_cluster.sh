./create-cluster clean
./create-cluster start
echo "yes" | ./create-cluster create
./create-cluster call RG.REFRESHCLUSTER
./create-cluster call RG.CONFIGSET ExecutionMaxIdleTime 300000
./create-cluster call CONFIG SET proto-max-bulk-len 2048mb
./create-cluster tailall
