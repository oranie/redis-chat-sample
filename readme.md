This project is internal trainning and demo app.

Redis and DynamoDB sample app


## Ranking
Redis : using sortedset data type

DynamoDB : PK + sort key

## Chat
Redis : using Stream data type


/chat/

client sent get request, get server status

/chat/comments/

comment function route
    
/chat/comments/add

client sent post request with name,comment txt, get response add comment status

POST value {'id':''oranie','comment':'hello world'}


/chat/comments/all

client sent get request, get all comment.
    
/chat/comments/latest

client sent get request with latest chat id, get the difference comment.

    

