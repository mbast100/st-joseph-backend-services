from controller.aws.dynamodb import DynamoDb
from data.media.schemas.media_input_schema import MediaInputSchema
from schema import SchemaError
from api_exception import ApiException



class Media(DynamoDb):

    def __init__ (self,params="", type="seasonal"):
        super().__init__(table_name="st_joseph_media") 
        self.params = params
        self.media_type = type
        self.media = ""
        self.error = ""
        self.message = ""

    @property
    def all(self):
        self.get_items_by_non_schema_key("type", self.media_type)
        return [self.item] if not self.items else self.items

    @property
    def save(self):
        if not self.params:
            return False
        if self.ok:
            try: 
               # if self.service_type == "seasonal" or  self.service_type == "regular" or self.service_type == "commemoration":
                self.create_media(self.params)
                return True
            except Exception as e:
                return False
        else:
            return False
    
    
    @property
    def ok(self):
        try:
            if self.media_type == "seasonal" or self.media_type == "regular"  or self.media_type ==  "commemoration" or self.media_type ==  "monthly-schedule":
                return MediaInputSchema(self.params).valid
            else :
                raise ApiException(
                "Invalid type '{}'.".format(self.self.media_type),400)
        except SchemaError:
            self.error =SchemaError.__dict__.get('__doc__')
            return False
