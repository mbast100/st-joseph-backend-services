from api_exception import ApiException
import re
import uuid


def generate_id():
    id = uuid.uuid4()
    return id


def valid_service_time_and_date(items):
    if len(items) == 0:
        raise ApiException("invalid serviceTimeAndDate", status_code=400)
    for item in items:

        if "date" not in item.keys():
            raise ApiException("invalid serviceTimeAndDate missing 'date'", status_code=400)
        if "start" not in item.keys():
            raise ApiException("invalid serviceTimeAndDate missing 'start'", status_code=400)

    return True


def valid_entries(entries, service):
    required_entries = entries
    if all(key in service for key in required_entries):
        return True
    else:
        return False


def validate_user_profile(profile):
    required_entries = ('first_name', 'last_name', "email","role","password")
    if valid_entries(required_entries, profile):
        return True
    else:
        raise ApiException(
            "missing required field, please make sure the following fields are present: {}".format(
                str(required_entries)),
            status_code=400)


def validate_regular_service(service):
    required_entries = ('displayName', 'serviceTimeAndDate',"name")
    if valid_entries(required_entries,service):
        serviceTimeAndDate = service["serviceTimeAndDate"]
        for item in serviceTimeAndDate:
            try:
                valid_service_time_and_date(service["serviceTimeAndDate"])
            except Exception as e:
                raise ApiException(e.__dict__.get("message"), status_code=400)
    else:
        raise ApiException(
            "missing required field, please make sure the following fields are present: {}".format(str(required_entries)),
            status_code=400)


def valid_seasonal_services(service):
    required_entries = ('title', 'display', 'services',"name", "month")
    if valid_entries(required_entries,service):
        services = service['services']
        if len(services) == 0:
            raise ApiException("please provide services offered for {}".format(service["title"]), status_code=400)
        for service in services:
            try:
                valid_service_time_and_date(service["serviceTimeAndDate"])
            except Exception as e:
                raise ApiException(e.__dict__.get("message"), status_code=400)
        return True
    else:
        raise ApiException(
            "missing required field, please make sure the following fields are present: {}".format(
                str(required_entries)),
            status_code=400)

def validate_email(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if not re.search(regex, email):
        return {"message": 'Invalid email format', "status_code": 400}


def validate_name(name):
    name = name.replace(' ', '')
    if not name.isalpha():
        return {"message": 'Invalid name format', "status_code": 400}
