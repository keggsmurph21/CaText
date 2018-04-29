import curses

import config as cfg

from cli_mode import Home, Lobby, Play


class CLI():
    def __init__(self):

        cfg.cli_logger.debug('CLI initializing ...')

        # set up curses screen
        self.stdscr = curses.initscr()
        self.stdscr.keypad(True)
        self.stdscr.refresh()
        curses.noecho()
        curses.cbreak()

        # use "mode"s to logically separate widget/data structure collections
        self.modes = {
            'home'  : Home('home')
        }
        self.change_mode('home')

        cfg.cli_logger.debug('... CLI initialized')

    def change_mode(self, mode, *args):
        cfg.cli_logger.debug('CLI changing mode (to {})'.format(mode))
        if mode not in self.modes:
            if mode == 'lobby':
                self.modes[mode] = Lobby(mode)
            elif 'play' in mode:
                self.modes[mode] = Play(mode)
        self.current_mode = self.modes[mode].set_as_current(*args)

    def add_line(self, string):
        cfg.cli_logger.debug('CLI adding a line to the current win_main')
        self.current_mode.win_main.add(string)

    def status(self, status):
        cfg.cli_logger.debug('CLI setting current win_status')
        self.current_mode.win_status.set(status)

    def input(self, prompt, visible=True, completions=None):
        cfg.cli_logger.debug('CLI prompting the user for input')
        return self.current_mode.win_input.listen(prompt=prompt, visible=visible, completions=completions)

    def wait(self):
        cfg.cli_logger.debug('CLI waiting')
        self.current_mode.win_input.wait()

    def quit(self):
        ''' wrapper for cleaning up our curses mode '''
        cfg.cli_logger.debug('CLI quitting')
        self.stdscr.keypad(False)
        curses.echo()
        curses.nocbreak()
        curses.endwin()
