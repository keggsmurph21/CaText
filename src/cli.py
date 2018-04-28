import curses

from cli_mode import Home, Lobby, Play

class CLI():
    def __init__(self, root_logger, env, get_path):

        # keep references to root logger and env manager
        self.logger = root_logger
        self.logger.debug('CLI initializing ...')
        self.env = env
        self.get_path = get_path

        # set up curses screen
        self.stdscr = curses.initscr()
        self.stdscr.keypad(True)
        self.stdscr.refresh()
        curses.noecho()
        curses.cbreak()

        # use "mode"s to logically separate widget/data structure collections
        self.modes = {
            'home'  : Home('home',  self.logger, self.env, self.get_path),
        }
        self.change_mode('home')

        self.logger.debug('... CLI initialized')

    def change_mode(self, mode, *args):
        self.logger.debug('changing mode (to {})'.format(mode))
        if mode not in self.modes:
            if mode == 'lobby':
                self.modes[mode] = Lobby(mode, self.logger, self.env, self.get_path)
            elif 'play' in mode:
                self.modes[mode] = Play(mode, self.logger, self.env, self.get_path)
        self.current_mode = self.modes[mode].set_as_current(*args)

    def add_line(self, string):
        self.logger.debug('adding a line to the current win_main')
        self.current_mode.win_main.add(string)

    def status(self, status):
        self.logger.debug('setting current win_status')
        self.current_mode.win_status.set(status)

    def input(self, prompt, visible=True, completions=None):
        self.logger.debug('prompting the user for input')
        return self.current_mode.win_input.listen(prompt=prompt, visible=visible, completions=completions)

    def wait(self):
        self.logger.debug('waiting for user keypress')
        self.current_mode.win_input.wait()

    def quit(self):
        ''' wrapper for cleaning up our curses mode '''
        self.logger.debug('quitting CLI')
        self.stdscr.keypad(False)
        curses.echo()
        curses.nocbreak()
        curses.endwin()
