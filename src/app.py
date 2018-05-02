import argparse
import json
import os
import sys

from curses import wrapper

import config as cfg

from api  import *
from cli  import *
from env  import Env
from log  import Logger
from user import User

__all__ = ['CaTexT', 'CaTexTError', 'play']

class CaTexT(object):
    def __init__(self, args={}):

        # root environment variable manager
        env_path = cfg.get_path('.env.ct')
        cfg.env = Env(env_path)
        cfg.env.set('CURRENT_USER','')
        cfg.env.set('PROJECT_ROOT', cfg.root)
        cfg.app = self

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
            cfg.cli.set_status('ERROR: {}'.format(e))
            cfg.cli.wait()
            raise CaTexTError(e)

        # get our new-game-form parameters
        with open(cfg.get_path('config','new_game_form.json')) as f:
            cfg.new_game_form = json.load(f)

        # initialize current_user to None (need it for self.loop())
        cfg.current_user = None

        cfg.app_logger.debug('... CaTexT initialized')

        self.loop()

    def logout(self):
        self.current_user = None
        cfg.current_user.logout()
        cfg.env.set('CURRENT_USER','')
        cfg.cli.change_mode('home')

    def loop(self):

        while True:

            # we need to be logged in to do anything
            if cfg.current_user is None:

                # try to get a user
                cfg.current_user = self.select_user()
                cfg.cli.set_status('Successfully logged in as {}'.format(cfg.current_user.name))
                cfg.env.set('CURRENT_USER', cfg.current_user.name)
                cfg.app_logger.info('current user: {}'.format(cfg.current_user.name))

                # go to the lobby
                cfg.app_logger.info('entering lobby')
                data = cfg.api.get_lobby(cfg.current_user.token)
                cfg.cli.change_mode('lobby', data)

            command, options, payload = self.parse(cfg.cli.input())

            if command == 'quit':
                self.quit()
            elif command == 'logout':
                self.logout()
            elif command == 'refresh':
                try:
                    data = cfg.api.get_lobby(cfg.current_user.token)
                    cfg.cli.change_mode('lobby', data)
                except APIError as e:
                    raise e
            elif command == 'new' or command == 'new_game':
                for param_type in cfg.new_game_form:
                    for param_name in cfg.new_game_form[param_type]:
                        param = cfg.new_game_form[param_type][param_name]
                        if param['short'] not in payload:
                            payload[param_name] = param['default']
                        else:
                            payload[param_name] = payload[param['short']]

                payload['action'] = 'new_game'
                try:
                    data = cfg.api.post_lobby(cfg.current_user.token, payload)
                    cfg.cli.change_mode('lobby', data)
                except APIError as e:
                    raise e
            else:
                message = 'Unrecognized command: {}'.format(command)
                cfg.app_logger.error(message)
                cfg.cli.set_status(message)

        #data = cfg.api.post_lobby(cfg.current_user.token, {'gameid':'5ae9cfbda992d5015715b046'})
        #print('data',data)

    def parse(self, string):

        cfg.app_logger.info('parsing string: "{}"'.format(string))
        words = string.split(' ')
        command = words[0]
        args = []
        kwargs = {}

        i = 1

        while i < len(words):

            word = words[i]
            if word[0] == '-':
                kwargs[word.strip('-')] = words[i+1]
                i += 2
            else:
                args.append(word)
                i += 1

        cfg.app_logger.info('parsed string: {}, {}, {}'.format(command, args, kwargs))
        return command, args, kwargs

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

            cfg.app_logger.debug('username: "{}" ({})'.format(username, len(username)))
            if user is None and len(username):
                password = cfg.cli.input(' - password: ', visible=False)
                cfg.app_logger.debug('attempting login (username={}, password={})'.format(username,'*'*len(password)))
                cfg.cli.set_status('Querying CatOnline database ... ')
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
                cfg.cli.set_status(str(e))
            elif isinstance(e, APIConnectionError):
                cfg.cli.set_status('ERROR: only local logins are available')
                cfg.cli.wait()

    def authenticate(self, username, password):
        ''' either use an authentication token or get a new one '''
        response = cfg.api.post_login(username, password)
        return response['user'], response['token']

    def parse_args(self):
        print('args',self.args)

    def quit(self):
        cfg.app_logger.info('CaTexT quitting')
        cfg.cli.quit()
        cfg.root_logger.info('goodbye')
        sys.exit(0)


class CaTexTError(Exception): pass


def play(args={}):

    app = CaTexT(args)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-a','--api', help='either `http` or `socketio`')
    parser.add_argument('-c','--cli', help='either `basic` or `curses`')
    parser.add_argument('--debug')
    parser.add_argument('--quiet')
    parser.add_argument('--set-default-user', help='set this user as the default')
    parser.add_argument('-u','--user', help='login as this user')
    parser.add_argument('--verbosity')
    parser.add_argument('--version')
    args = vars(parser.parse_args()) # convert to dictionary

    play(args)
