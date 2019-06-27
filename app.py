from chalice import Chalice
from rediscluster import StrictRedisCluster
from datetime import datetime
import os

app = Chalice(app_name='helloworld')




@app.route('/')
def index():
    print(os.environ['REDIS_ENDPOINT'])
    print(os.environ['REDIS_PORT'])
    try:
        #startup_nodes = [{"host": "oranie-cluster.ab0uwo.clustercfg.apne1.cache.amazonaws.com", "port": "7000"}]
        startup_nodes = [{"host": os.environ['REDIS_ENDPOINT'], "port": os.environ['REDIS_PORT']}]
        rc = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True, skip_full_coverage_check=True,socket_timeout=1, socket_connect_timeout=1)
    except Exception as e:
        print(e)

    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    rc.set("key1", now)

    result = rc.get("key1")
    return {'hello': result}



# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
