from boto3.dynamodb.conditions import Key, Attr

from app import dynamodb

table = dynamodb.Table("services")


def update_item_by_name(name):
    table.update_item(
        Key={
            'name': name,
        },
        UpdateExpression='SET age = :val1',
        ExpressionAttributeValues={
            ':val1': 26
        }
    )