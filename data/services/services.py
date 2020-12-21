from controller.aws.dynamodb import DynamoDb
from data.services.schemas.seasonal_service_input_schema import SeasonalServiceInputSchema
from data.services.schemas.regular_services_input_schema import RegularServiceInputSchema
from schema import SchemaError
from api_exception import ApiException


class Services(DynamoDb):

    def __init__(self, params="", type="seasonal"):
        super().__init__(table_name="services")
        self.params = params
        self.service_type = type
        self.service = ""
        self.error = ""
        self.message = ""

    @property
    def all(self):
        self.get_items_by_non_schema_key("type", self.service_type)
        return [self.item] if not self.items else self.items

    @property
    def exists(self):
        if self.ok and self.params["name"]:
            if self.service_exists(self.params["name"]):
                self.message = self._message
                return True
        elif self.name:
            return self.service_exists(self.name)            
        else:
            return False

    def find_by(self, key, value):
        if key != "name":
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

    def update(self, updates, name=""):
        if not isinstance(updates, dict):
            return False
        if not name:
            name = self.name 
        try:
            if not self.service:
                self.update_service(name, updates)
            else:
                self.update_service(self.service[0]["name"], updates)
            self.message = "Updated {}.".format(name)
            return True
        except Exception as e:
            raise e

    @property
    def delete(self):
        if not self.params:
            self.message = "Missing 'name' param for delete operation."
            return False
        try:
            self.delete_by_schema_key("name", self.params["name"])
            return True if self.status_code == 200 else False
        except Exception as e:
            return False

    def delete_all(self,items):
        try:
            self.delete_batch(items,"name")
            self.message = "Items deleted."
        except Exception as e:
            print(e.__dict__)
        
    @property
    def save(self):
        if not self.params:
            return False
        if self.ok:
            try:
                if self.service_type == "seasonal":
                    self.create_seasonal_service(self.params)
                elif self.service_type == "regular" or self.service_type == "commemoration":
                    self.create_service(self.params, self.service_type)
                return True
            except Exception as e:
                return False
        else:
            return False

    @property
    def name(self):
        try:
            if self.service:
                return self.service[0]["name"]
            else:
                return self.params["name"]
        except KeyError:
            return ""
        

    @property
    def ok(self):
        try:
            if self.service_type == "seasonal" or self.service_type == "commemoration":
                return SeasonalServiceInputSchema(self.params).valid
            elif self.service_type == "regular":
                return RegularServiceInputSchema(self.params).valid
            else:
                raise ApiException(
                    "Invalid type '{}'.".format(self.service_type), 400)
        except SchemaError:
            self.error = SchemaError.__dict__.get('__doc__')
            return False
