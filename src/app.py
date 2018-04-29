import os
import sys

from curses import wrapper

import config as cfg

from api  import API, APIError, APIConnectionError, APIInvalidDataError
from cli  import CLI
from env  import Env
from log  import Logger
from user import User

class CaTexT():
    def __init__(self):

        # need a consistent reference to the root of this directory
        cfg.root = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))

        # root environment variable manager
        env_filepath = cfg.get_path('env.ct')
        cfg.env = Env(env_filepath)
        cfg.env.set('CURRENT_USER','')

        # make some loggers
        logs_path = cfg.get_path('logs')
        if not(os.path.exists(logs_path)):
            os.mkdir(logs_path)
        cfg.root_logger = Logger('ROOT')
        cfg.app_logger = Logger('APP')
        cfg.app_logger.debug('initializing CaTexT ...')

        # make sure we have a path to hold our user data
        users_path = cfg.get_path('.users')
        cfg.env.set('users_path', users_path)
        if not(os.path.exists(users_path)):
            cfg.app_logger.debug('creating ".users" directory')
            os.mkdir(users_path)

        # set up our "GUI" which is really just a curses CLI
        cfg.cli_logger = Logger('CLI')
        cfg.cli = CLI()

        # set up the interface w/ our REST API
        try:
            protocol = cfg.env.get('PROTOCOL', 'http')
            host = cfg.env.get('HOST', 'localhost')
            port = cfg.env.get('PORT', 49160)
            cfg.api_logger = Logger('API')
            cfg.api = API(protocol, host, port)
        except APIError as e:
            cfg.app_logger.critical(e)
            cfg.cli.status('ERROR: {}'.format(e))
            cfg.cli.wait()
            raise CaTexTError(e)

        # try to get a user
        cfg.current_user = self.select_user()
        cfg.cli.status('Successfully logged in as {}'.format(cfg.current_user.name))
        cfg.env.set('CURRENT_USER', cfg.current_user.name)
        cfg.app_logger.info('current user: {}'.format(cfg.current_user.name))

        cfg.app_logger.debug('... CaTexT initialized')

    def enter_lobby(self):

        cfg.app_logger.info('entering lobby')
        data = cfg.api.get_lobby(cfg.current_user.token)
        cfg.cli.change_mode('lobby', data)

        cfg.cli.wait()

    def select_user(self):
        '''
        generates a list of available users to select from, or enables
        the user to login thru the web endpoint

        @return User() corresponding to the choice
        '''

        cfg.app_logger.debug('selecting user')
        default_user = cfg.env.get('DEFAULT_USER')
        cfg.app_logger.debug('default user: {}'.format(default_user))
        user = self.get_user(default_user)

        while user is None:

            cfg.app_logger.debug('unable to log in with default user')
            username = cfg.cli.input(' - username: ')
            user = self.get_user(username)

            if user is None and len(username):
                password = cfg.cli.input(' - password: ', visible=False)
                cfg.app_logger.debug('attempting login (username={}, password={})'.format(username,'*'*len(password)))
                cfg.cli.status('Querying CatOnline database ... ')
                user = self.save_user(username, password)

        return user

    def get_user(self, name):
        if name == None:
            return None
        return User().read(name)

    def save_user(self, username, password):
        try:
            user_data, token = self.authenticate(username, password)
            return User().set(user_data, token)
        except APIError as e:
            cfg.app_logger.error(e)
            if isinstance(e, APIInvalidDataError):
                cfg.cli.status(str(e))
            elif isinstance(e, APIConnectionError):
                cfg.cli.status('ERROR: only local logins are available')
                cfg.cli.wait()


    def authenticate(self, username, password):
        ''' either use an authentication token or get a new one '''
        return cfg.api.post_login(username, password)

    def quit(self):
        cfg.app_logger('quitting CaTexT')
        cfg.cli.quit()

class CaTexTError(Exception): pass


def main(*args, **kwargs):

    app = CaTexT()
    app.enter_lobby()
    app.quit()


if __name__ == '__main__':
    wrapper(main)
