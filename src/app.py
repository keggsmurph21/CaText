import argparse
import os
import sys

from curses import wrapper

import config as cfg

from api  import choose_api, APIError, APIConnectionError, APIInvalidDataError
from cli  import choose_cli, CLIError
from env  import Env
from log  import Logger
from user import User

class CaTexT():
    def __init__(self, args={}):

        # root environment variable manager
        env_filepath = cfg.get_path('.env.ct')
        cfg.env = Env(env_filepath)
        cfg.env.set('CURRENT_USER','')
        cfg.env.set('PROJECT_ROOT', cfg.root)

        # evaluate passed arguments (dictionary)
        self.args = args
        self.parse_args()

        # make some loggers
        logs_path = cfg.get_path('logs')
        if not(os.path.exists(logs_path)):
            os.mkdir(logs_path)
        cfg.root_logger = Logger('ROOT')
        cfg.app_logger = Logger('APP')
        cfg.app_logger.debug('initializing CaTexT ...')

        # make sure we have a path to hold our user data
        users_path = cfg.get_path('.users')
        cfg.env.set('USERS_ROOT', users_path)
        if not(os.path.exists(users_path)):
            cfg.app_logger.debug('creating ".users" directory')
            os.mkdir(users_path)

        # set up our "GUI" which is really just a (curses) CLI
        cli = cfg.env.get('CLI_TYPE','curses')
        cfg.cli_logger = Logger('CLI')
        cfg.cli = choose_cli(cli)()

        # set up the interface w/ our REST API
        try:
            api = cfg.env.get('API_TYPE','http')
            cfg.api_logger = Logger('API')
            cfg.api = choose_api(api)()
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

    def parse_args(self):
        print(self.args)

    def quit(self):
        cfg.app_logger.info('CaTexT quitting')
        cfg.cli.quit()
        cfg.root_logger.info('goodbye')


class CaTexTError(Exception): pass


def main(*args, **kwargs):

    parser = argparse.ArgumentParser()
    parser.add_argument('-a','--api', help='either `http` or `socketio`')
    parser.add_argument('-c','--cli', help='either `basic` or `curses`')
    parser.add_argument('--debug')
    parser.add_argument('--quiet')
    parser.add_argument('--set-default-user', help='set this user as the default')
    parser.add_argument('-u','--user', help='login as this user')
    parser.add_argument('-v', action='count', default=0)
    args = vars(parser.parse_args()) # convert to dictionary

    app = CaTexT(args)
    app.enter_lobby()
    app.quit()


if __name__ == '__main__':
    main()#wrapper(main)
