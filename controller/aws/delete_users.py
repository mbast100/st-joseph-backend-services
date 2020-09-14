import boto3
from boto3.dynamodb.conditions import Key
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')


def delete_users(id):
    response = table.scan(**{'FilterExpression': Key('id').eq(id)})
    list = response['Items']
    if len(list) != 0:
        email = list[0].get("email")
        table.delete_item(
            Key={
                "email": email
            }
        )
        return {"message": 'User deleted successfully', "status_code": 200}
    elif len(list) == 0:
        return {"message": 'User not found.', "status_code": 404}
