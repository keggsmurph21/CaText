import getpass
import json
import os
import requests

WEBROOT = 'http://localhost:49160'
URI_API_LOGIN = os.path.join(WEBROOT, 'api', 'login')
URI_API_LOBBY = os.path.join(WEBROOT, 'api', 'lobby')

class API():
    def __init__(self):
        print('API connection initialized ...')
        self.token = None

    def post_login(self):
        username = input('username: ')
        password = getpass.getpass('password: ')
        payload = { 'username':username, 'password':password }

        try:
            res = requests.post(URI_API_LOGIN, data=payload)

            if res.status_code == 200:
                self.token = json.loads(res.text)['token']
                return self.token
            else:
                print('invalid username or password')
                return None

        except requests.exceptions.ConnectionError:
            print('unable to connect to server')
            return None

    def get_lobby(self):
        headers = { 'x-access-token':self.token }

        try:
            res = requests.get(URI_API_LOBBY, headers=headers)

            if res.status_code == 200:
                print(res.text)
            else:
                print(json.loads(res.text)['message'])

        except requests.exceptions.Conn/ectionError:
            print('unable to connect to server')

    def post_lobby(self, data):
        pass

    def get_play(self):
        pass

    def post_play(self, data):
        pass
