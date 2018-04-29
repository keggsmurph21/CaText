from __future__ import print_function

import curses
import getpass
import os
import sys

import config as cfg

cli_module_path = cfg.get_path('src','cli_modules')
sys.path.append(cli_module_path)
from mode import Home, Lobby, Play


def choose_cli(name):
    if name == 'basic':
        return Basic
    elif name == 'curses':
        return Curses
    else:
        raise CLIError('Unknown interface ({})'.format(name))


class CLI(object):
    def __init__(self):     raise NotImplementedError
    def change_mode(self):  raise NotImplementedError
    def add_line(self):     raise NotImplementedError
    def status(self):       raise NotImplementedError
    def input(self):        raise NotImplementedError
    def wait(self):         raise NotImplementedError
    def quit(self):         raise NotImplementedError


class Curses(CLI):
    def __init__(self):

        cfg.cli_logger.debug('CLI initializing (Curses) ...')

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

    def input(self, prompt=None, visible=True, completions=None):
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


class Basic(CLI):
    def __init__(self):

        cfg.cli_logger.debug('CLI initializing (Basic) ...')

        # primitive modes
        self.modes = {
            'home' : {
                'set_as_current' : (lambda: print('Log in with your CatOnline credentials'))
            },
            'lobby' : {
                'set_as_current' : (lambda: print('You are now in the CaTexT lobby'))
            },
            'play'  : {
                'set_as_current' : (lambda: print('You are now playing CaTexT'))
            }
        }
        self.change_mode('home')

        cfg.cli_logger.debug('... CLI initialized')

    def change_mode(self, mode, *args):
        cfg.cli_logger.debug('CLI changing mode (to {})'.format(mode))
        self.current_mode = self.modes[mode]
        self.current_mode['set_as_current']()

    def add_line(self, string):
        cfg.cli_logger.debug('CLI adding a line to the current win_main')
        print(string)

    def status(self, status):
        cfg.cli_logger.debug('CLI setting current win_status')
        print(status)

    def input(self, prompt='', visible=True, completions=None):
        cfg.cli_logger.debug('CLI prompting the user for input')
        if visible:
            return input(prompt)
        else:
            return getpass.getpass(prompt)

    def wait(self):
        cfg.cli_logger.debug('CLI waiting')
        input('press <Enter> to continue ...')

    def quit(self):
        cfg.cli_logger.debug('CLI quitting')


class CLIError(Exception): pass
