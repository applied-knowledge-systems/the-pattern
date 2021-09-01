PROTECTED_MODE=no
PORT=30000
NODES=$(cat /proc/cpuinfo| grep cores | wc -l)
REPLICAS=1
ADDITIONAL_OPTIONS="--loadmodule /home/alex/infrastructure/RedisGears/bin/linux-x64-release/redisgears.so  PythonInstallationDir /home/alex/infrastructure/RedisGears/bin/linux-x64-release/python3_1.0.3 CreateVenv 1 DownloadDeps 1"