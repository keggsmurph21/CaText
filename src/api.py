import json
import os
import requests

import config as cfg


def choose_api(name):
    if name == 'http':
        return HTTP
    elif name == 'socketio':
        return SocketIO
    else:
        raise APIError('Unknown interface ({})'.format(name))


class API():
    def __init__(self):     raise NotImplementedError
    def get_uri(self):      raise NotImplementedError
    def post_login(self):   raise NotImplementedError
    def get_lobby(self):    raise NotImplementedError
    def post_lobby(self):   raise NotImplementedError
    def get_play(self):     raise NotImplementedError
    def post_play(self):    raise NotImplementedError


class HTTP(API):
    def __init__(self):

        cfg.api_logger.debug('API initializing ...')

        protocol = cfg.env.get('PROTOCOL', 'http')
        host = cfg.env.get('HOST', 'localhost')
        port = cfg.env.get('PORT', 49160)

        # save webroot as combination of these
        self.webroot = '{}://{}:{}'.format(protocol, host, port)

        cfg.api_logger.debug('... API initialized (webroot: {})'.format(self.webroot))

    def get_uri(self, path):
        ''' get a URI for API endpoint '''
        return os.path.join(self.webroot, 'api', path)

    def post_login(self, username, password):
        '''
        post to the $WEBROOT/api/login endpoint
        note: this function prompts the user for password

        @return auth token or None
        '''

        payload = { 'username':username, 'password':password }
        uri = self.get_uri('login')

        try:
            # hit the endpoint
            cfg.api_logger.info('post {} (payload: {})'.format(uri, json.dumps(payload)))
            res = requests.post(uri, data=payload)
            cfg.api_logger.info('response code {}'.format(res.status_code))

            if res.status_code == 200:
                # valid response
                token = json.loads(res.text)['token']
                user  = json.loads(res.text)['user']
                cfg.api_logger.debug('user {} got auth token {}'.format(user, token))

                return user, token
            else:
                # something went wrong
                raise APIInvalidDataError('Invalid username or password')

        except requests.exceptions.ConnectionError:
            raise APIConnectionError('Unable to connect to server at "{}"'.format(uri))

    def get_lobby(self, token):
        '''
        query $WEBROOT/api/lobby endpoint

        @return data
        '''

        # make sure we include our auth token
        headers = { 'x-access-token':token }
        uri = self.get_uri('lobby')

        try:
            # hit the endpoint
            cfg.api_logger.info('get {} (token: {})'.format(uri, token))
            res = requests.get(uri, headers=headers)
            cfg.api_logger.info('response code {}'.format(res.status_code))

            if res.status_code == 200:
                # valid response
                cfg.api_logger.info('lobby response: {}'.format(res.text))
            else:
                # something went wrong
                raise APIInvalidDataError(json.loads(res.text)['message'])

        except requests.exceptions.ConnectionError:
            raise APIConnectionError('Unable to connect to server at "{}"'.format(uri))

    def post_lobby(self, token, data):
        pass

    def get_play(self):
        pass

    def post_play(self, data):
        pass


class SocketIO(API):
    pass

class APIError(Exception): pass
class APIConnectionError(APIError): pass
class APIInvalidDataError(APIError): pass
