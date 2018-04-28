import os

from api  import API
from env  import Env
from user import User

def CaText():
    def __init__(self):
        self.env = Env(../.env)
        self.api = API()

        print('Welcome to CaText')

        self.authenticate()

    def authenticate():
        token = self.env.get('CATONLINE_TOKEN')
        while token is None:
            token = self.api.post_login()

        self.env.set('CATONLINE_TOKEN', token)


if __name__ == '__main__':

    app = CaText()
