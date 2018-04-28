import os

from env import Env

class User():

    def __init__(self, project_root, logger):

        # references
        self.project_root = project_root
        self.logger = logger
        self.logger.debug('Bootstrapping new User ...')

    def set(self, data, token):

        # grab some data from the response
        self.name = data['name']
        self.data = data

        # grab the token
        self.token = token

        # the root of where we're going to store our data
        self.path = os.path.join(self.project_root, '.users', self.name)
        if not(os.path.exists(self.path)):
            self.logger.debug('... creating new user: {}'.format(self.name))
            os.mkdir(self.path)
            os.mkdir(os.path.join(self.path, 'games'))
        else:
            self.logger.debug('... user already exists, overwriting')

        self.write()

    def write(self):

        self.logger.info('writing user data for {}'.format(self.name))

        e = Env(os.path.join(self.path, 'data.ct'))
        for key in self.data:
            e.set(key, self.data[key])

        with open(os.path.join(self.path, 'token'), 'w') as f:
            f.write(self.token)

    def read(self, name):

        self.logger.debug('... reading in user data for {}'.format(name))

        self.name = name
        self.path = os.path.join(self.project_root, '.users', self.name)

        e = Env(os.path.join(self.path, 'data.ct'))
        self.data = e.variables

        with open(os.path.join(self.path, 'token')) as f:
            self.token = f.read()
