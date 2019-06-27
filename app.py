from chalice import Chalice
from datetime import datetime
from chalicelib.redis import create_connection

app = Chalice(app_name='helloworld')

@app.route('/')
def index():
    rc = create_connection()

    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    rc.set("key1", now)

    result = rc.get("key1")
    return {'status': 'server is good!  ' + result}

@app.route('/chat/comment/add',methods=['POST'])
def comment_add():
    user_as_json = app.current_request.json_body
    print(user_as_json)

    rc = create_connection()
    response_xadd = rc.xadd("chat", "*", 100,{"name": "data"})
    print(response_xadd)

    response_xrange = rc.xrange("chat","-","+")

    print(response_xrange)

    return {'state' : 'Commment add OK.comment seq id is '+ response_xadd}

@app.route('/chat/comment/all')
def comment_list_get():
    rc = create_connection()
    response = rc.xrange("chat","-","+")

    return {response}

@app.route('/chat/comment/latest',methods=['POST'])
def comment_list_get():
    rc = create_connection()

    return {'':''}




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
