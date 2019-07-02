from chalice import Chalice
from datetime import datetime
from chalicelib.redis import StreamStrictRedisCluster
from chalicelib.redis import create_connection
import json

app = Chalice(app_name='chalice-nosql-sample')


@app.route('/', cors=True)
def index():
    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    rc = create_connection()
    rc.set("key1", now)
    result = rc.get("key1")

    return {'status': 'server is good!  ' + result}
    # return {'status': 'server is good!  ' + now}

@app.route('/chat/comments/add', methods=['POST'], cors=True)
def comment_add():
    body = app.current_request.json_body
    print(body)

    rc = create_connection()

    response_xadd = rc.xadd("chat", "*", "key", {body['name']: body['comment']})
    return {'state': 'Commment add OK', "comment_seq_id": response_xadd}


@app.route('/chat/comments/all', methods=['GET'], cors=True)
def comment_list_get():
    rc = create_connection()

    response = rc.xrange("chat", "-", "+")
    return {'response': response}


@app.route('/chat/comments/latest', methods=['GET'], cors=True)
def comment_list_get():
    rc = create_connection()

    response = rc.xrevrange("chat", "+", "-", "COUNT", "20")
    return {'response': response}


@app.route('/chat/comments/latest/{latest_seq_id}', methods=['GET'], cors=True)
def comment_list_get(latest_seq_id):
    latest_list = latest_seq_id.split('-')
    #print(latest_list)

    next_id = int(latest_list[1])
    next_id += 1
    next_seq_id = f'{latest_list[0]}-{next_id}'
    print(next_seq_id)

    rc = create_connection()
    response = rc.xrange("chat", next_seq_id, "+")

    return {'response': response}
