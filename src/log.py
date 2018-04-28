import datetime
import os
import sys

class Logger():

    def __init__(self, name, project_root, env):

        self.name = name

        verbosity = env.get('VERBOSITY','CRITICAL')
        debug = True if env.get('DEBUG') == '1' else 0

        levels = ['CRITICAL','ERROR','WARN','INFO','DEBUG']
        try:
            self.level = levels.index(verbosity)
            self.level_name = levels[self.level]
        except ValueError:
            print('LoggerError: invalid level: {}'.format(level))
            self.level = 1
            self.level_name = 'INVALID_LOGGING_LEVEL'

        self.logs_path = os.path.join(project_root, 'logs')
        if not(os.path.exists(self.logs_path)):
            os.mkdir(self.logs_path)

        self.force_debug = debug or self.level == 4

        self.write(message='\n\n\n')
        self.debug('Logger initializing (level: {}, debug: {})'.format(self.level_name, self.force_debug))


    def format(self, show_time=True, prefix=None, message=''):

        str = ''
        if show_time:
            str += '[{}] '.format(get_time())
        str += '{} '.format(self.name)
        if prefix is not None:
            str += '{}: '.format(prefix)
        str += message
        str += '\n'

        return str


    def write(self, file='main', message=''):
        
        file_path = os.path.join(self.logs_path, '{}.log'.format(file))
        with open(file_path, 'a') as f:
            f.write(message)


    def handle(self, message, file, prefix, level):

        message = self.format(prefix=prefix, message=message)

        if self.level >= level:
            sys.stderr.write(message)
            if file != 'main':
                self.write(file=file, message=message)
        if self.force_debug or self.level >= level:
            self.write(message=message)

    def critical(self, message, file='main'):
        self.handle(message, file, 'CRITICAL', 0)

    def error(self, message, file='main'):
        self.handle(message, file, 'ERROR', 1)

    def warn(self, message, file='main'):
        self.handle(message, file, 'WARN', 2)

    def info(self, message, file='main'):
        self.handle(message, file, 'INFO', 3)

    def debug(self, message, file='main'):
        self.handle(message, file, 'DEBUG', 4)


    def put(self, message):
        print(message)


def get_time():
    return str(datetime.datetime.now())
