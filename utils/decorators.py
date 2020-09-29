def authorize_req(user_roles=[]):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            current_user_role = get_current_user(resource='role')
            if current_user_role in user_roles:
                return func(*args, **kwargs)
            else:
                raise ApiException('Access Denied', status_code=401)
        return decorated_function
    return 