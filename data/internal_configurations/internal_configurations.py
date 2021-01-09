from controller.aws.dynamodb import DynamoDb
from schema import SchemaError
from api_exception import ApiException
from data.internal_configurations.schemas.internal_configurations_schemas import InternalConfigurationsSchema
import datetime


class InternalConfigurations(DynamoDb):

    def __init__(self, feature="", params=""):
        super().__init__(table_name="st_joseph_internal_configurations", schema_key='feature')
        self.params = params
        self.feature = feature
        self.error = ""
        self.internal_configurations = ''
        self.message = ""

    @property
    def all(self):
        self.get_all_items()
        return [self.item] if not self.items else self.items

    @property
    def exists(self):
        feature = self.feature or self.params["feature"]
        self.find(self._schema_key, self.feature)

        if self.item or self.items:
            return True
        else:
            return False

    def find_by(self, key, value):
        if key != self._schema_key:
            self.get_items_by_non_schema_key(key, value)
        else:
            self.find(key, value)
        self.internal_configuration = [
            self.item] if not self.items else self.items
        if self.internal_configuration == ['']:
            return []
        return [self.item] if not self.items else self.items

    def where(self, params):
        self._where(params)
        self.service = [self.item] if not self.items else self.items
        if self.service == ['']:
            return []
        return [self.item] if not self.items else self.items

    def update(self, updates, feature=""):
        if not isinstance(updates, dict) or (not self.feature and not self.params):
            return False
        if not feature:
            feature = self.feature or self.params["feature"]
        try:
            if self.exists:
                updates["updated_on"] = str(datetime.datetime.now())
                self._update(feature, updates)
                self.message = "Updated {}.".format(feature)
                return True
            else:
                return False
        except Exception as e:
            return False

    @property
    def delete(self):
        if not self.params:
            self.message = "Missing 'name' param for delete operation."
            return False
        try:
            self.delete_by_schema_key(self._schema_key, self.params["feature"])
            return True if self.status_code == 200 else False
        except KeyError:
            raise ApiException("Missing `feature` in request body.", 400)
        except Exception as e:
            return False

    def delete_all(self, items):
        try:
            self.delete_batch(items, "name")
            self.message = "Items deleted."
        except Exception as e:
            print(e.__dict__)

    @property
    def save(self):
        if not self.params:
            return False
        if self.ok:
            try:
                self.params["created_on"] = str(datetime.datetime.now())
                self.create(self.params)
                return True
            except Exception as e:
                return False
        else:
            return False

    @property
    def ok(self):
        try:
            InternalConfigurationsSchema(self.params).valid
            return True
        except SchemaError:
            self.error = SchemaError.__dict__.get('__doc__')
            return False
