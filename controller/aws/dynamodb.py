from app import dynamodb
from botocore.exceptions import *
from boto3.dynamodb.conditions import Key, Attr
from controller.aws.helpers import *


class DynamoDb():
    def __init__(self, table_name):
        self.table_name = table_name
        self.table = dynamodb.Table(table_name)
        self.response = {}

    def create(self, item):
        self.response = self.table.put_item(
            Item=item
        )

    def update_service(self, name, updates):
        for update in updates.keys():
            try:
                self.table.update_item(
                    Key={
                        'name': name
                    },
                    UpdateExpression="set {} = :r".format(update),
                    ExpressionAttributeValues={
                        ':r': updates[update],
                    },
                    ReturnValues="UPDATED_NEW"
                )
            except ClientError:
                print(ClientError.__dict__())
                raise ApiException("oops", 400)

    def get_all_items(self):
        self.response = self.table.scan()

    def get_item_by_name(self, name):
        self.response = self.table.get_item(Key={'name': name})

    def get_item_by_email(self, email):
        self.response = self.table.get_item(Key={'email': email})

    def get_items_by_type(self, type):
        self.response = self.table.scan(FilterExpression=Attr('type').eq(type))

    def create_seasonal_service(self, service):
        valid_seasonal_services(service)
        service.update({"type": "seasonal"})
        self.create(service)

    def create_regular_service(self, service):
        validate_regular_service(service)
        service.update({"type": "regular"})
        self.create(service)

    def delete(self, name):
        self.response = self.table.delete_item(Key={"name": name})

    def service_exists(self, name):
        self.get_item_by_name(name)
        print(self.response)
        if self.item == "item not found":
            return False
        else:
            return True

    def user_exists(self, email):
        self.get_item_by_email(email)
        if self.item == "item not found":
            return False
        else:
            return True

    @property
    def status_code(self):
        return self.response["ResponseMetadata"]["HTTPStatusCode"]

    @property
    def items(self):
        try:
            return self.response["Items"]
        except KeyError:
            return "items not found"

    @property
    def item(self):
        try:
            return self.response["Item"]
        except KeyError:
            return "item not found"
