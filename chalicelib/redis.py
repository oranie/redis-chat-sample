from rediscluster import StrictRedisCluster
import os
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def create_connection():
    endpoint = os.environ['REDIS_ENDPOINT']
    port = os.environ['REDIS_PORT']
    startup_node = [{'host': endpoint, 'port': port}]
    print(startup_node)
    rc = StreamStrictRedisCluster(startup_nodes=startup_node, decode_responses=True, skip_full_coverage_check=True,
                                  socket_timeout=1, socket_connect_timeout=1)

    return rc


class StreamStrictRedisCluster(StrictRedisCluster):
    # def __init__(self,):
    #   super(StreamStrictRedisCluster, self).__init__()

    # response_xadd = rc.xadd('chat', '*', 100, {body['name']: body['comment']})
    def xadd(self, stream, seq_id, name, name_value, comment, comment_value):
        args = ['XADD', stream, seq_id, name, name_value, comment, comment_value]
        logging.info('XADD params : %s', args)
        response = self.execute_command(*args)
        return response

    # response = rc.xrange('chat', '-', '+')
    def xrange(self, stream, start, end, COUNT=None, count_number=None):
        if COUNT is not None:
            args = ['XRANGE', stream, start, end, COUNT, count_number]
        else:
            args = ['XRANGE', stream, start, end]

        logging.info('XRANGE params : %s', args)
        response = self.execute_command(*args)
        return response

    # response = rc.xrevrange('chat', '+', '-', 'COUNT', '50')
    def xrevrange(self, stream, start, end, COUNT=None, count_number=None):
        if COUNT is not None:
            args = ['XREVRANGE', stream, start, end, COUNT, count_number]
        else:
            args = ['XREVRANGE', stream, start, end]

        logging.info('XREVRANGE params : %s', args)
        response = self.execute_command(*args)
        return response
