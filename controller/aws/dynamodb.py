from app import dynamodb
from botocore.exceptions import *
from boto3.dynamodb.conditions import Key, Attr
from controller.aws.helpers import *
from datetime import date
import uuid


class DynamoDb():
    def __init__(self, table_name):
        self.table_name = table_name
        self.table = dynamodb.Table(table_name)
        self.response = {}
        self._error = ''
        self._message = ''
        self.today = date.today()

    def create(self, item):
        try:
            self.response = self.table.put_item(
                Item=item
            )
        except Exception as e:
            print(e)
            raise ApiException(
                "oops something wrong while create the service", status_code=500)

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

    def update_internal_configuration(self, feature, updates):

        for update in updates.keys():
            try:
                self.table.update_item(
                    Key={
                        'feature': feature
                    },
                    UpdateExpression="set {} = :r".format(update),
                    ExpressionAttributeValues={
                        ':r': updates[update],
                    },
                    ReturnValues="UPDATED_NEW"
                )
            except ClientError as error:
                self.response = error.response
                raise ApiException(self.response["Error"], 400)

            except Exception as e:
                print(e)
                raise ApiException("oops", 500)

    def get_internal_configurations(self, feature=""):
        if feature:
            self.response = self.table.get_item(Key={'feature': feature})
        else:
            self.response = self.table.scan()

    def get_all_items(self):
        self.response = self.table.scan()

    def get_item_by_name(self, name):
        self.response = self.table.get_item(Key={'name': name})

    def get_item_by_key(self, key):
        self.response = self.table.get_item(Key={'key': key})

    def get_items_by_month(self, month):
        self.response = self.table.scan(
            FilterExpression=Attr('month').eq(month))

    def get_item_by_email(self, email):
        self.response = self.table.get_item(Key={'email': email})

    def get_items_by_type(self, type):
        self.response = self.table.scan(FilterExpression=Attr('type').eq(type))

    def get_items_by_type_and_month(self, type, month):
        self.response = self.table.scan(
            FilterExpression=Attr("type").eq(type) & Attr("month").eq(month))

    def _where(self, params={}):
        keys = list(params.keys())
        self.response = self.table.scan(
            FilterExpression=Attr(keys[0]).eq(params[keys[0]]) & Attr(keys[1]).eq(params[keys[1]]))

    def find(self, key, value):
        self.response = self.table.get_item(Key={key: value})

    def get_items_by_non_schema_key(self, key, value):
        self.response = self.table.scan(
            FilterExpression=Attr(key).eq(value))

    def create_seasonal_service(self, service):
        try:
            valid_seasonal_services(service)
            service.update({"type": "seasonal"})
            self.create(service)
        except Exception as e:
            raise ApiException(e.__dict__.get("message"), 400)

    def create_regular_service(self, service):
        try:
            validate_regular_service(service)
            service.update({"type": "regular"})
            self.create(service)
        except Exception as e:
            raise ApiException(e.__dict__.get("message"), 400)

    def create_commemoration(self, service):
        try:
            valid_seasonal_services(service)
            service.update({"type": "commemoration"})
            service.update({"createdOn": self.today.strftime("%d/%m/%Y")})
            self.create(service)
        except Exception as e:
            raise ApiException(e.__dict__.get("message"), 400)

    def create_service(self, service, service_type):
        try:
            service.update({"type": service_type})
            self.create(service)
        except Exception as e:
            raise ApiException(e.__dict__.get("message"), 400)

    def create_media(self, media):
        try:
            self.create(media)
        except Exception as e:
            raise ApiException(e.__dict__.get("message"), 400)

    def delete_by_schema_key(self, key, value):
        self.response = self.table.delete_item(Key={key: value})

    def delete_batch(self, keys, schema_key):
        for key in keys:
            self.delete_by_schema_key(schema_key, key)

    def service_exists(self, name):
        self.get_item_by_name(name)
        exists = True if self.item else False
        if exists:
            self._message = "Duplicate service name for '{}'".format(name)
        return exists

    def internal_configuration_exists(self, feature):
        self.get_internal_configurations(feature=feature)
        if not self.item and not self.items:
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
            return ""

    @property
    def item(self):
        try:
            return self.response["Item"]
        except KeyError:
            return ""

    @property
    def sorted_items(self):
        if self.items != "items not found":
            return sorted(self.items, lambda i: i["month"])

    def generate_id(self):
        id = uuid.uuid4()
        return str(id)
