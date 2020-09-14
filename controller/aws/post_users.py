import boto3
from controller.aws.helpers import *
from controller.aws.validation import *
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')


def post_users(payload):
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

    response = table.query(
        KeyConditionExpression=(Key('email').eq(email))
    )
    list = response['Items']
    if len(list) != 0:
        return {"message": 'User with this email already exists', "status_code": 406}

    email_validation = validate_email(email)
    if (email_validation is not None) and (email_validation['status_code'] == 400):
        return {"message": 'Invalid email format', "status_code": 400}

    first_name_validation = validate_name(first_name)
    if (first_name_validation is not None) and (first_name_validation['status_code'] == 400):
        return {"message": 'Invalid first_name format', "status_code": 400}

    last_name_validation = validate_name(last_name)
    if (last_name_validation is not None) and (last_name_validation['status_code'] == 400):
        return {"message": 'Invalid last_name format', "status_code": 400}

    id = generate_id()
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
    return {"message": 'User created successfully', "status_code": 201}
