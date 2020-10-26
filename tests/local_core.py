from app import app
from urllib.parse import urlencode


class ClientInstanceCore:

    def __init__(self, host='localhost', admin=False):
        self.host = host
        self.client = app.test_client()
        self.json_response = {}
        self.response = ''
        self.admin = admin

    def core(self, action, url, data='', params='', token='', cookie='', headers='', custom_headers=False):
        
        if self.admin:
            headers = {
                "Authorization": token
            }

        res = ''
        if action == 'GET':
            if params:
                res = self.client.get(url+"?"+urlencode(params), headers=headers)
            else:
                res = self.client.get(url, headers=headers)

        elif action == 'POST':
            if data:
                if params:
                    res = self.client.post(url+"?"+urlencode(params), json=data, headers=headers)
                else:
                    res = self.client.post(url, json=data, headers=headers)
        elif action == 'DELETE':
            if params:
                res = self.client.delete(url + "?" + urlencode(params), json=data, headers=headers)
            else:
                res = self.client.delete(url, json=data, headers=headers)

        self.response = res
        try:
            self.json_response = res.json
        except Exception as e:
            self.json_response = "Something went wrong :"+self.response
        if self.status_code != 200 or self.status_code != 201:
            print(self.json_response)
        return res

    @property
    def status_code(self):
        try:
            return self.response.status_code
        except KeyError:
            return ''

    @property
    def message(self):
        try:
            return self.json_response.get('message')
        except KeyError:
            return ''

    @property
    def username(self):
        return self.user_property.get('username')
