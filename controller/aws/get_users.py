import boto3
from boto3.dynamodb.conditions import Key
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')


def get_all_users():
    response = table.scan()
    list = response['Items']
    return list


def get_user_by_id(id):
    response = table.scan(**{'FilterExpression': Key('id').eq(id)})
    list = response['Items']
    if len(list) != 0:
        return {"message": list, "status_code": 200}
    else:
        return {"message": "User not found.", "status_code": 404}
