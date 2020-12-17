from controller.aws.dynamodb import DynamoDb
from data.services.schemas.seasonal_service_input_schema import SeasonalServiceInputSchema
from data.services.schemas.regular_services_input_schema import RegularServiceInputSchema
from schema import SchemaError


class Services(DynamoDb):

    def __init__(self, params="", type="seasonal"):
        super().__init__(table_name="services")
        self.params = params
        self.type = type
        self.service =""

    @property
    def all(self):
        self.get_items_by_non_schema_key("type", self.type)
        return [self.item] if not self.items else self.items

    @property
    def exists(self):
        if self.params["name"] and self.ok:
            return self.service_exists(self.params["name"])
        else:
            return False

    def find_by(self, key, value):
        if key != "name":
            self.get_items_by_non_schema_key(key, value)
        else:
            self.where(key, value)
        self.service = [self.item] if not self.items else self.items
        return [self.item] if not self.items else self.items

    def update(self,updates, name=""):
        if not isinstance(updates, dict):
            return False
        try:
            if name:
                self.update_service(name, updates)
            elif self.service:
                self.update_service(self.service[0]["name"], updates)
            return True
        except Exception as e:
            raise e
        
    @property
    def save(self):
        if not self.params:
            return False
        if self.ok:
            try:
                if self.type == "seasonal":
                    self.create_seasonal_service(self.params)
                elif self.type == "regular":
                    self.create_regular_service(self.params)
                return True
            except Exception as e:
                return False
        else:
            return False

    @property
    def ok(self):
        try:
            if self.type == "seasonal":
                return SeasonalServiceInputSchema(self.params).valid
            elif self.type == "regular":
                return RegularServiceInputSchema(self.params).valid
        except SchemaError:
            return False
