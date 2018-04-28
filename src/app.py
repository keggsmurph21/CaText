import os

from api  import API, APIError
from env  import Env
from log  import Logger
from user import User

class CaText():
    def __init__(self):

        self.root_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),'..'))

        self.env = Env(os.path.join(self.root_path, '.env'))
        self.logger = Logger(self.root_path, self.env)
        self.api = API(self.logger, self.env)

        self.logger.put('Welcome to CaText')

        self.authenticate()

    def authenticate(self):
        token = self.env.get('CATONLINE_TOKEN')
        while token is None:
            try:
                token = self.api.post_login()
            except APIError:
                pass

        self.env.set('CATONLINE_TOKEN', token)


if __name__ == '__main__':


    app = CaText()
    print(os.path.abspath(os.path.dirname(__file__)))
