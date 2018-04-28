import os

from api  import API
from env  import Env
from user import User

def authenticate(api, env):
    token = env.get('CATONLINE_TOKEN')
    while token is None:
        token = api.post_login()

    env.set('CATONLINE_TOKEN', token)


if __name__ == '__main__':

    env = Env('./.env')
    api = API()

    authenticate(api, env)
