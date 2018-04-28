import getpass
import json
import os
import requests

class API():
    def __init__(self, root_logger, env):

        # keep a reference to the root logger
        self.logger = root_logger
        self.logger.debug('API initializing ...')

        # keep a reference to the root environment variables
        self.env = env

        # try to get a webroot
        self.webroot = env.get('WEBROOT')
        if self.webroot is None:
            raise APIError('Unable to parse webroot')

        # initialize auth token
        self.token = None

        self.logger.debug('API initialized (webroot: {})'.format(self.webroot))

    def get_uri(self, path):
        ''' get a URI for API endpoint '''
        return os.path.join(self.webroot, 'api', path)

    def post_login(self):
        '''
        post to the $WEBROOT/api/login endpoint
        note: this function prompts the user for password

        @return auth token or None
        '''

        # get all the fields we need for our request
        username = input('username: ')
        password = getpass.getpass('password: ')
        payload = { 'username':username, 'password':password }
        uri = self.get_uri('login')

        try:
            # hit the endpoint
            res = requests.post(uri, data=payload)

            if res.status_code == 200:
                # valid response
                self.token = json.loads(res.text)['token']
                return self.token
            else:
                # something went wrong
                raise APIInvalidDataError('Invalid username or password')

        except requests.exceptions.ConnectionError:
            raise APIError('Unable to connect to server at "{}"'.format(uri))

    def get_lobby(self):
        '''
        query $WEBROOT/api/lobby endpoint

        @return data
        '''

        # make sure we include our auth token
        headers = { 'x-access-token':self.token }
        uri = self.get_uri('lobby')

        try:
            # hit the endpoint
            res = requests.get(uri, headers=headers)

            if res.status_code == 200:
                # valid response
                print(res.text)
            else:
                # something went wrong
                raise APIInvalidDataError(json.loads(res.text)['message'])

        except requests.exceptions.ConnectionError:
            raise APIError('Unable to connect to server at "{}"'.format(uri))

    def post_lobby(self, data):
        pass

    def get_play(self):
        pass

    def post_play(self, data):
        pass

class APIError(Exception):
    pass

class APIInvalidDataError(APIError):
    pass
