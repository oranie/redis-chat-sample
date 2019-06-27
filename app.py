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

@app.route('/chat/comments/add',methods=['POST'],cors=True)
def comment_add():
    method = app.current_request.method
    if method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Method': 'GET,OPTIONS',
            'Access-Control-Allow-Origin': ','.join(_ALLOWED_ORIGINS),
            'Access-Control-Allow-Headers': 'X-Some-Header',
        }
        origin = app.current_request.headers.get('origin', '')
        if origin in _ALLOWED_ORIGINS:
            headers.update({'Access-Control-Allow-Origin': origin})
        return Response(
            body=None,
            headers=headers,
        )
    elif method == 'POST':
        body = {
        }
        raw_body = app.current_request.raw_body.decode()
        body = json.loads(raw_body)
        print(body)

        rc = create_connection()
        response_xadd = rc.xadd("chat", "*", 100,{body['name']:body['comment']})
        print(response_xadd)

        response_xrange = rc.xrange("chat","-","+")
        print(response_xrange)

        return {'state' : 'Commment add OK',"comment_seq_id": response_xadd}

@app.route('/chat/comments/all',methods=['GET'],cors=True)
def comment_list_get():
    rc = create_connection()
    response = rc.xrange("chat","-","+")

    return {'response': response}

@app.route('/chat/comments/latest/{seq_id}',methods=['GET'],cors=True)
def comment_list_get(seq_id):
    request = app.current_request

    rc = create_connection()
    response = rc.xrange("chat",seq_id,"+")

    return {'response':response}


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
