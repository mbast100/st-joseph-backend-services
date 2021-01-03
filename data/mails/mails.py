from controller.aws.dynamodb import DynamoDb
from data.mails.schemas.mails_schema import MailsSchema
from schema import SchemaError
from api_exception import ApiException
import datetime


class Mails(DynamoDb):

    def __init__(self, params=''):
        super().__init__(table_name="st_joseph_mails")
        self.params = params
        self.error = ""
        self.schema_key = 'id'

    @property
    def all(self):
        self.get_all_items()
        return [self.item] if not self.items else self.items

    # @property
    # def exists(self):
    #     if self.ok and self.params["email"]:
    #         if self.service_exists(self.params["name"]):
    #             self.message = self._message
    #             return True
    #     elif self.name:
    #         return self.service_exists(self.name)
    #     else:
    #         return False

    def find_by(self, key, value):
        if key != "id":
            self.get_items_by_non_schema_key(key, value)
        else:
            self.find(key, value)
        self.service = [self.item] if not self.items else self.items
        if self.service == ['']:
            return []
        return [self.item] if not self.items else self.items

    def where(self, params):
        self._where(params)
        self.service = [self.item] if not self.items else self.items
        if self.service == ['']:
            return []
        return [self.item] if not self.items else self.items

    @property
    def delete(self):
        if not self.params:
            self.message = "Missing 'name' param for delete operation."
            return False
        try:
            self.delete_by_schema_key(
                self.schema_key, self.params[self.schema_key])
            return True if self.status_code == 200 else False
        except Exception as e:
            return False

    def delete_all(self, items):
        try:
            self.delete_batch(items, self.schema_key)
            self.message = "Items deleted."
        except Exception as e:
            print(e.__dict__)

    @property
    def save(self):
        if not self.params:
            return False
        if self.ok:
            try:
                self.params['id'] = self.generate_id()
                self.params['created_on'] = str(datetime.datetime.now())
                self.create(self.params)
                return True
            except Exception as e:
                print(e)
                return False
        else:
            self.error = "Schema validation failed."
            return False

    @property
    def ok(self):
        try:
            MailsSchema(self.params).valid
            return True
        except SchemaError:
            self.error = SchemaError.__dict__.get('__doc__')
            return False

    @property
    def full_name(self):
        return self.params['full_name']

    @property
    def email(self):
        return self.params['email']

    @property
    def message(self):
        return self.params['message']

    @property
    def phone_number(self):
        return self.params['phone_number']
