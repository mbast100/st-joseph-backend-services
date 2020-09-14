import boto3
from boto3.dynamodb.conditions import Key
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')


def put_users(payload, id):
    keys_list = payload.keys()

    if 'email' in keys_list:
        email = payload['email']
    else:
        return {"message": 'Missing email in payload', "status_code": 406}

    if 'password' in keys_list:
        password = payload['password']
    else:
        return {"message": 'Missing password in payload', "status_code": 406}

    if 'first_name' in keys_list:
        first_name = payload['first_name']
    else:
        return {"message": 'Missing first_name in payload', "status_code": 406}

    if 'last_name' in keys_list:
        last_name = payload['last_name']
    else:
        return {"message": 'Missing last_name in payload', "status_code": 406}

    if 'role' in keys_list:
        role = payload['role']
    else:
        return {"message": 'Missing role in payload', "status_code": 406}

    if 'id' in keys_list:
        id = payload['id']
    else:
        return {"message": 'Missing id in payload', "status_code": 406}

    response = table.scan(**{'FilterExpression': Key('id').eq(id)})
    list = response['Items']
    if len(list) != 0:
        old_email = list[0].get("email")
        table.delete_item(
            Key={
                "email": old_email
            }
        )
        table.put_item(
            Item={
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
                "role": role,
                "email": email,
                "id": str(id)
            }
        )
        return {"message": 'User updated successfully', "status_code": 200}
    elif len(list) == 0:
        return {"message": 'User not found.', "status_code": 404}
