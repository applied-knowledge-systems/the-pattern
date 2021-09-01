Mapping UMLS CUI to Canonical Name 
unzip with 
tar jxvf redis_cui_canonical_names.tar.bz2

populate Redis instance 
redis-cli -p 9001 -h 127.0.0.1 --pipe < redis_canonical.txt 
it will create a CUI:NAME mapping via standard redis SET command

If you want to make changes check out [sql import](https://github.com/AlexMikhalev/cord19redisknowledgegraph/tree/master/sql_import) 