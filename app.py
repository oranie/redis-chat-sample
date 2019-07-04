from chalice import Chalice, Response
from datetime import datetime
from chalicelib.redis import StreamStrictRedisCluster
from chalicelib.redis import create_connection, stream_data_to_json
import logging
import os
import re

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

app = Chalice(app_name='chalice-nosql-sample')


@app.route('/', cors=True)
def index():
    # server status check URI
    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    rc = create_connection()
    rc.set('key1', now)
    result = rc.get('key1')

    return {'status': 'server is good!  ' + result}


@app.route('/chat', cors=True)
def chat():
    # Demo html
    html = open("./chalicelib/livechat.html", "r")
    base_lines = html.read()
    if os.environ['REDIS_ENDPOINT'] == 'localhost':
        print('local dayo')
        lines = base_lines
    else:
        lines = re.sub('http://localhost:8000/', 'https://xgc5p4eaah.execute-api.ap-northeast-1.amazonaws.com/api/',
                       base_lines)

    html.close()

    return Response(body=str(lines), status_code=200,
                    headers={'Content-Type': 'text/html', "Access-Control-Allow-Origin": "*"})


@app.route('/chat/comments/add', methods=['POST'], cors=True)
def comment_add():
    body = app.current_request.json_body
    logging.info('add request POST request Body : %s', body)

    rc = create_connection()

    response_xadd = rc.xadd('chat', '*', 'name', body['name'], 'comment', body['comment'])
    return {'state': 'Commment add OK', 'comment_seq_id': response_xadd}


@app.route('/chat/comments/all', methods=['GET'], cors=True)
def comment_list_get():
    rc = create_connection()

    response = rc.xrange('chat', '-', '+')
    return {'response': stream_data_to_json(response)}


@app.route('/chat/comments/latest', methods=['GET'], cors=True)
def comment_list_get():
    rc = create_connection()

    response = rc.xrevrange('chat', '+', '-', 'COUNT', '20')
    logging.info('latest response : %s', response)

    return {'response': stream_data_to_json(response)}


@app.route('/chat/comments/latest/{latest_seq_id}', methods=['GET'], cors=True)
def comment_list_get(latest_seq_id):
    latest_list = latest_seq_id.split('-')
    logging.info('latest comments GET request latest seq id : %s', *latest_list)

    # Increment redis streams data type latest seq id
    # To get next comments
    next_id = int(latest_list[1])
    next_id += 1
    next_seq_id = f'{latest_list[0]}-{next_id}'
    logging.info('next seq id : %s', next_seq_id)

    rc = create_connection()
    response = rc.xrange('chat', next_seq_id, '+')
    logging.info('latest comments next id response : %s', response)

    return {'response': stream_data_to_json(response)}
