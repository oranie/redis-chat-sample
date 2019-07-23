import os
import logging
import boto3
from boto3.dynamodb.conditions import Key, Attr
import datetime

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

class DdbChat():
    def createConnection(self, tableName):
        ddb = boto3.resource('dynamodb')
        ddb_table = ddb.Table(tableName)

        return ddb_table


    def putComment(self,table,name,comment,chat_room):
        logging.info('PutComments params : %s %s %s %s',table, name, comment, chat_room)

        now = datetime.datetime.now()
        chat_seq_time = int(now.timestamp())

        table.put_item(
            Item={
                'name': name,
                'time': chat_seq_time,
                'comment': comment,
                'chat_room': chat_room
            }
        )
        return

    def getLatestComments(self,table,chat_room):
        logging.info('getLatestComments params : %s %s', table, chat_room)

        response = table.query(
            IndexName='chat_room_time_idx',
            Select='ALL_ATTRIBUTES',
            KeyConditionExpression=Key('chat_room').eq(chat_room),
            ScanIndexForward=False,
            Limit=20
        )

        return response

    def getRangeComments(self, table, chat_room, position):
        logging.info('getRabgeComments params : %s %s %s', table, chat_room, str(position))

        result = []

        response = table.query(
            IndexName='chat_room_time_idx',
            Select='ALL_ATTRIBUTES',
            KeyConditionExpression=Key('chat_room').eq(chat_room) & Key('time').gt(position),
            ScanIndexForward=False
        )
        for index, item in enumerate(response['Items']):
            result.append(item)

        while 'LastEvaluatedKey' in response:
            print('LastEvaluatedKey Hit!!!')
            response = table.query(
                IndexName='chat_room_time_idx',
                Select='ALL_ATTRIBUTES',
                KeyConditionExpression=Key('chat_room').eq(chat_room) & Key('time').gt(position),
                ScanIndexForward=False
            )

            for index, item in enumerate(response['Items']):
                result.append(item)


        return result

    def getAllComments(self,table,chat_room):
        logging.info('getAllComments params : %s %s', table, chat_room)

        result = []

        response = table.query(
            IndexName='chat_room_time_idx',
            Select='ALL_ATTRIBUTES',
            KeyConditionExpression=Key('chat_room').eq(chat_room),
            ScanIndexForward=False
        )

        for index, item in enumerate(response['Items']):
            result.append(item)

        while 'LastEvaluatedKey' in response:
            print('LastEvaluatedKey Hit!!!')
            response = table.query(
                IndexName='chat_room_time_idx',
                Select='ALL_ATTRIBUTES',
                KeyConditionExpression=Key('chat_room').eq(chat_room),
                ScanIndexForward=False
            )

            for index, item in enumerate(response['Items']):
                result.append(item)

        return result

if __name__ == "__main__":
    ddb = DdbChat()
    table = ddb.createConnection('chat')

    name = 'oranie'
    comment = 'チャットシステムです'
    chat_room = 'chat'

    ddb.putComment(table, name, comment, chat_room)
    result = ddb.getLatestComments(table, chat_room)

    list = result['Items']
    for index, item in enumerate(list):
        logging.info('id: ' + str(index) + ' name:' + item['name'] + ' time:' + str(item['time']) + ' comment:'+ item['comment'])

    result = ddb.getAllComments(table, chat_room)
    for index, item in enumerate(result):
        logging.info('ALL Result ' + 'id: ' + str(index) + ' name:' + item['name'] + ' time:' + str(item['time']) + ' comment:'+ item['comment'])

    logging.info(result)

    result = ddb.getRangeComments(table, chat_room, 0)

    for index, item in enumerate(result):
        logging.info('RANGE Result ' + 'id: ' + str(index) + ' name:' + item['name'] + ' time:' + str(item['time']) + ' comment:'+ item['comment'])

    logging.info(result)


