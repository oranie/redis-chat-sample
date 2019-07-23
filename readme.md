## This project is internal trainning and demo app.

Redis sample app

## Envroiment
Redis 5.0+

Python 3.7.3+

Redis Cluster mode launch (local,production. Not supported non cluster mode)

Please read Chalice project doc.
https://github.com/aws/chalice

## Deploy
local test
```$xslt
 chalice local --stage local
```
redis port 7000

deploy
```$xslt
chalice deploy
```
redis port 6379


## Chat
Redis : using Stream data type


* /chat

chat client HTML page 

### API
    
* /chat/comments/add

client sent post request with name,comment txt, get response add comment status

POST value {'name':''oranie','comment':'hello world'}


* /chat/comments/all

client sent get request, get all comment.
    
* /chat/comments/latest

client sent get request latest 20 comments.

* /chat/comments/latest/{latest_seq_id}

client sent get request with latest chat id, get the difference comments.
    

