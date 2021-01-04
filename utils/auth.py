from api_exception import ApiException
from utils.web import HTTPcore
from flask import request
from functools import wraps

unprotected_path = ['/api/mails/contact']

def validate_token():
    if request.path in unprotected_path:
        return True
        
    token = request.headers.get("Authorization")
    if not token:
        raise ApiException("Missing authorization token.", status_code=401)
    
    web = HTTPcore(
        "https://xb54882p49.execute-api.us-east-1.amazonaws.com/prod/api/login", 
        )
    web.core("PUT", headers={"Authorization": token})

    if web.get_status_code == 200:
        return True
    else:
        return False



