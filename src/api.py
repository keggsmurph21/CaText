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


class API(object):
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
        return self.post(uri, payload)

    def get_lobby(self, token):
        '''
        query $WEBROOT/api/lobby endpoint

        @return data
        '''

        # make sure we include our auth token
        headers = { 'x-access-token':token }
        uri = self.get_uri('lobby')
        return self.get(uri, headers)

    def post_lobby(self, token, payload):
        '''
        post to the $WEBROOT/api/lobby endpoint
        note: this function prompts the user for password

        @return data
        '''

        # make sure we include our auth token
        headers = { 'x-access-token':token }
        uri = self.get_uri('lobby')
        return self.post(uri, payload, headers)

    def get_play(self):
        pass

    def post_play(self, payload):
        pass

    def get(self, uri, headers={}):
        try:
            # hit the endpoint
            cfg.api_logger.info('get {}'.format(uri))
            res = requests.get(uri, headers=headers)
            cfg.api_logger.info('response code: {}'.format(res.status_code))

            if res.status_code == 200:
                # valid response
                cfg.api_logger.debug('response: {}'.format(res.text))
                return json.loads(res.text)
            else:
                # something went wrong
                raise APIInvalidDataError(res.text)

        except requests.exceptions.ConnectionError:
            raise APIConnectionError('Unable to connect to server at "{}"'.format(uri))

    def post(self, uri, payload, headers={}):
        try:
            # hit the endpoint
            cfg.api_logger.info('post {} (payload: {})'.format(uri, json.dumps(payload)))
            res = requests.post(uri, data=payload, headers=headers)
            cfg.api_logger.info('response code: {}'.format(res.status_code))

            if res.status_code == 200:
                # valid response
                cfg.api_logger.debug('response: {}'.format(res.text))
                return json.loads(res.text)
            else:
                # something went wrong
                raise APIInvalidDataError(res.text)

        except requests.exceptions.ConnectionError:
            raise APIConnectionError('Unable to connect to server at "{}"'.format(uri))


class SocketIO(API):
    pass

class APIError(Exception): pass
class APIConnectionError(APIError): pass
class APIInvalidDataError(APIError): pass
