from chalice import Chalice
from datetime import datetime
from chalicelib.redis import create_connection
import json

app = Chalice(app_name='helloworld')


@app.route('/')
def index():
    rc = create_connection()

    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    rc.set("key1", now)

    result = rc.get("key1")
    return {'status': 'server is good!  ' + result}


@app.route('/chat/comments/add', methods=['POST'], cors=True)
def comment_add():
    raw_body = app.current_request.raw_body.decode()
    body = json.loads(raw_body)
    print(body)

    rc = create_connection()
    response_xadd = rc.xadd("chat", "*", 100, {body['name']: body['comment']})

    return {'state': 'Commment add OK', "comment_seq_id": response_xadd}


@app.route('/chat/comments/all', methods=['GET'], cors=True)
def comment_list_get():
    rc = create_connection()
    response = rc.xrange("chat", "-", "+")

    return {'response': response}


@app.route('/chat/comments/latest', methods=['GET'], cors=True)
def comment_list_get():
    rc = create_connection()
    response = rc.xrevrange("chat", "+", "-", "COUNT", "50")

    return {'response': response}


@app.route('/chat/comments/latest/{latest_seq_id}', methods=['GET'], cors=True)
def comment_list_get(latest_seq_id):
    latest = latest_seq_id.split('-')
    print(latest)

    next_id = int(latest[1])
    next_id += 1
    next_seq_id = f'{latest[0]}-{next_id}'
    print(next_seq_id)

    rc = create_connection()
    response = rc.xrange("chat", next_seq_id, "+")

    return {'response': response}

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
