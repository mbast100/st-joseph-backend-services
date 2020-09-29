import requests
import json


class HTTPcore():

    def __init__(self, url):
        self._url = url
        self.json_response = {}
        self.error = ''
        self.tar = ''
        self.spotify_res =''
        self._r = requests
        self._headers = {
            'Content-Type': "application/json",
        }
    
    def core(self, action, custom_url='', headers='', data='', params='',auth='', **kwargs):

        res = None
        _headers = self._headers
        if headers:
            _headers.update(headers)
        if params:
            if custom_url:
                res = self._r.request(action, custom_url, headers=_headers, data=data, auth=auth, params=params)
                print("request sent , response :", res)
            else:
                res = self._r.request(action,self._url, headers=_headers, data=data,auth=auth, params=params)
        else:
            if custom_url:
                res = self._r.request(action, custom_url, headers=_headers, data=data, auth=auth)
            else:
                res = self._r.request(action, self._url, headers=_headers, data=data,auth=auth)
        try:
            self.json_response = res.json()
        except json.JSONDecodeError:
            print('caught json decode error in request')
            self.json_response = {'message':'no json response available'}

        self.tar = res
        return res

    def format_json(self,keys=[],**kwargs):

        if len(keys) == 0:
            keys =['uri']
        items = self.items
        new_items=[]
        for item in items:
            mod = {x: item[x] for x in keys}
            new_items.append(mod)
        return new_items

    def set_url(self, url):
        self._url = url

    @property
    def items(self):
        try:
            return self.json_response['items']
        except KeyError:
            return ''
    
    @property
    def access_token(self):
        try:
            return self.json_response.get('access_token')
        except KeyError:
            return ""

    @property
    def get_status_code(self):
        try:
            return self.tar.status_code
        except Exception as e:
            return ''
    @property
    def get_token_type(self):
        try:
            return self.json_response.get('token_type')
        except Exception as e:
            raise Exception("Missing token_type")
    
    @property
    def get_scope(self):
        try:
            return self.json_response.get('scope')
        except Exception as e:
            raise Exception('Missing scope.')
    
    @property
    def refresh_token(self):
        try:
            return self.json_response.get("refresh_token")
        except KeyError:
            return ""

    @property
    def get_expires_in(self):
        return self.json_response.get("expires_in")
    
    @property
    def get_error_code(self):
        error = self.json_response.get('error')
        return error.get('status')
    
    @property
    def get_error_message(self):
        try:
            error = self.json_response.get('error')
            return error.get('message')
        except KeyError:
            return ""