import os
import sys

from api  import API, APIError, APIInvalidDataError
from env  import Env
from log  import Logger
from user import User

class CaText():
    def __init__(self):

        # need a consistent reference to the root of this directory
        self.project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__),'..'))

        # root environment variable manager
        self.env = Env(self.get_path('.env.ct'))

        # root logger
        self.logger = Logger('MAIN', self.project_root, self.env)

        # set up the interface w/ our REST API
        try:
            self.api = API(self.logger, self.env)
        except APIError:
            self.logger.critical('Cannot locate server, exiting ...')
            sys.exit(-1)

        # welcome message
        self.logger.put('\n\n<< Welcome to CaTexT >>')

        # make sure we have a path to hold our user data
        self.users_path = self.get_path('.users')
        if not(os.path.exists(self.users_path)):
            self.logger.debug('creating ".users" directory')
            os.mkdir(self.users_path)

        # TODO: replace this
        self.authenticate()

    def get_path(self, *paths):
        ''' get path under project root '''
        return os.path.join(self.project_root, *paths)

    def authenticate(self):
        ''' either use an authentication token or get a new one '''

        token = self.env.get('CATONLINE_TOKEN')
        while token is None:
            try:
                token = self.api.post_login()
            except APIError as e:
                self.logger.error(str(e))
                if isinstance(e, APIInvalidDataError):
                    self.logger.put(str(e))

        self.env.set('CATONLINE_TOKEN', token)


if __name__ == '__main__':

    app = CaText()
