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

        # choose a user from /.users/ or add a new one
        self.current_user = self.select_user()
        self.logger.info('selected {}'.format(self.current_user.name))

        self.cli.quit()

    def select_user(self):
        '''
        generates a list of available users to select from, or enables
        the user to login thru the web endpoint

        @return User() corresponding to the choice
        '''

        self.cli.dialog.print_line('Choose a user profile (use arrow keys and <Enter> to choose):')
        new_user_str = '<login from web>'
        available_users = [new_user_str] + os.listdir(self.get_path('.users'))
        choice = self.cli.dialog.prompt_from_list(available_users)

        if choice == new_user_str:
            return self.add_new_user()
        else:
            return self.get_user(choice)


    def get_path(self, *paths):
        ''' get path under project root '''
        return os.path.join(self.project_root, *paths)

    def get_user(self, name):
        user = User(self.project_root, self.logger)
        user.read(name)
        return user

    def add_new_user(self):
        user_data, token = self.authenticate()
        user = User(self.project_root, self.logger)
        user.set(user_data, token)
        return user

    def authenticate(self):
        ''' either use an authentication token or get a new one '''

        self.cli.dialog.print_line('Login with your CatOnline credentials')
        token = None

        while token is None:
            try:
                username, password = self.cli.dialog.prompt_credentials()
                self.logger.debug('username:{}, password:{}'.format(username,['*' for i in password]))
                return self.api.post_login(username, password)
            except APIError as e:
                self.logger.error(str(e))
                if isinstance(e, APIInvalidDataError):
                    self.cli.dialog.print_line('{}, please try again'.format(str(e)))

        #self.env.set('CATONLINE_TOKEN', token)


if __name__ == '__main__':

    app = CaText()
