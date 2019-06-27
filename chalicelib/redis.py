from rediscluster import StrictRedisCluster

import os

def create_connection():
    startup_nodes = [{"host": os.environ['REDIS_ENDPOINT'], "port": os.environ['REDIS_PORT']}]
    rc = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True, skip_full_coverage_check=True,socket_timeout=1, socket_connect_timeout=1)

    return rc

    #try:
    #startup_nodes = [{"host": "oranie-cluster.ab0uwo.clustercfg.apne1.cache.amazonaws.com", "port": "7000"}]
    #print('now comment is ' + response)
    #except Exception as e:
    #    print(e)