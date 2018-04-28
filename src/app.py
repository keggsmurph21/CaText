import os
import sys

from api  import API, APIError, APIInvalidDataError
from env  import Env
from cli  import CLI
from log  import Logger
from user import User

class CaText():
    def __init__(self):

        # need a consistent reference to the root of this directory
        self.project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__),'..'))

        # root environment variable manager
        self.env = Env(self.get_path('env.ct'))

        # root logger
        self.logger = Logger('MAIN', self.project_root, self.env)

        # set up our "GUI" which is really just a curses CLI
        self.cli = CLI(self.logger, self.env)

        # set up the interface w/ our REST API
        try:
            self.api = API(self.logger, self.env)
        except APIError:
            self.logger.critical('Cannot locate server, exiting ...')
            sys.exit(-1)

        # make sure we have a path to hold our user data
        self.users_path = self.get_path('.users')
        if not(os.path.exists(self.users_path)):
            self.logger.debug('creating ".users" directory')
            os.mkdir(self.users_path)

        # try to get a user ... first check defaults
        self.current_user = self.select_user()

        self.logger.info('current user: {}'.format(self.current_user.name))

    def select_user(self):
        '''
        generates a list of available users to select from, or enables
        the user to login thru the web endpoint

        @return User() corresponding to the choice
        '''

        default_user = self.env.get('DEFAULT_USER')
        self.logger.debug('default user: {}'.format(default_user))
        user = self.get_user(default_user)

        if user is None:
            self.cli.status('Log in with your CatOnline credentials')

        while user is None:

            username = self.cli.input(' - username: ')
            user = self.get_user(username)

            if user is None:
                password = self.cli.input(' - password: ', visible=False)
                self.logger.debug('username:{}, password:{}'.format(username,'*'*len(password)))
                self.cli.status('Querying CatOnline database ... ')
                user = self.save_user(username, password)

        self.cli.status('Successfully logged in as {}'.format(user.name))
        self.logger.debug(user.token)
        return user

    def get_path(self, *paths):
        ''' get path under project root '''
        return os.path.join(self.project_root, *paths)

    def get_user(self, name):
        if name == None:
            return None
        return User(self.project_root, self.logger).read(name)

    def save_user(self, username, password):
        try:
            user_data, token = self.authenticate(username, password)
            return User(self.project_root, self.logger).set(user_data, token)
        except APIError as e:
            self.logger.error(e)
            if isinstance(e, APIInvalidDataError):
                self.cli.status(str(e))


    def authenticate(self, username, password):
        ''' either use an authentication token or get a new one '''
        return self.api.post_login(username, password)


class CaTextError(Exception):
    pass


if __name__ == '__main__':

    app = CaText()
    app.cli.quit()
