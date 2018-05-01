from __future__ import print_function

import curses
import getpass
import os
import shutil
import sys

from curses import wrapper

import config as cfg

cli_module_path = cfg.get_path('src','cli_modules')
sys.path.append(cli_module_path)
from mode import *
from window import *

__all__ = ['choose_cli', 'CLIError']

def choose_cli(name):
    if name == 'basic':
        return Basic
    elif name == 'curses':
        return Curses
    else:
        raise CLIError('Unknown interface ({})'.format(name))


class CLI(object):
    def __init__(self):
        cfg.cli = self

        self.set_width()

        home_mode = Home('home')
        self.current_mode = home_mode
        self.modes = {
            'home'  : home_mode
        }

    def set_width(self):
        terminal_size = shutil.get_terminal_size((80,26))
        cfg.env.set('TERM_WIDTH', terminal_size[0])

    def change_mode(self, mode, *args): raise NotImplementedError

    def set_main(self, strings):
        cfg.cli_logger.debug('CLI adding lines to the current win_main')
        for string in strings:
            self.add_main(string)

    def set_banner(self, string):   raise NotImplementedError
    def add_main(self):             raise NotImplementedError
    def set_status(self, string):   raise NotImplementedError

    def input(self):        raise NotImplementedError
    def wait(self):         raise NotImplementedError
    def quit(self):         raise NotImplementedError


class Curses(CLI):
    def __init__(self):

        cfg.cli_logger.debug('Curses CLI initializing ...')
        super(Curses, self).__init__()

        # set up curses stuff
        self.stdscr = curses.initscr()
        self.stdscr.keypad(True)
        self.stdscr.refresh()
        curses.noecho()
        curses.cbreak()
        self.init_windows()

        # print the stuff from the Home mode
        self.current_mode.set_as_current()

        cfg.cli_logger.debug('... Curses CLI initialized')

    def init_windows(self):
        # set up the curses windows
        self.current_mode.win_banner = StripWindow(y=0)
        SeparatorWindow(y=1)
        self.current_mode.win_main = ScrollWindow(y=2, height=curses.LINES-5)
        SeparatorWindow(y=curses.LINES-3)
        self.current_mode.win_status = StripWindow(y=curses.LINES-2)
        self.current_mode.win_input = InputWindow(y=curses.LINES-1, scrollwindow=self.current_mode.win_main)

    def change_mode(self, mode, *args):
        cfg.cli_logger.debug('CLI changing mode (to {})'.format(mode))
        if mode not in self.modes:
            if mode == 'lobby':
                self.modes[mode] = Lobby(mode)
            elif 'play' in mode:
                self.modes[mode] = Play(mode)
            self.current_mode = self.modes[mode]
            self.init_windows()
            self.current_mode.set_as_current(*args)
        else:
            self.current_mode = self.modes[mode].set_as_current(*args)

    def set_banner(self, string):
        cfg.cli_logger.debug('CLI setting the current win_banner')
        self.current_mode.win_banner.set(string)

    def add_main(self, string):
        cfg.cli_logger.debug('CLI adding a line to the current win_main')
        self.current_mode.win_main.add(string)

    def set_status(self, string):
        cfg.cli_logger.debug('CLI setting current win_status')
        self.current_mode.win_status.set(string)

    def input(self, prompt=None, visible=True, completions=None):
        cfg.cli_logger.debug('CLI prompting the user for input')
        return self.current_mode.win_input.listen(prompt=prompt, visible=visible, completions=completions)
        #return wrapper(lambda x: self.current_mode.win_input.listen(prompt=prompt, visible=visible, completions=completions))

    def wait(self):
        cfg.cli_logger.debug('CLI waiting')
        wrapper(self.current_mode.win_input.wait)

    def quit(self):
        ''' wrapper for cleaning up our curses mode '''
        cfg.cli_logger.debug('CLI quitting')
        self.stdscr.keypad(False)
        curses.echo()
        curses.nocbreak()
        curses.endwin()


class Basic(CLI):
    def __init__(self):

        cfg.cli_logger.debug('Basic CLI initializing ...')

        self.flash_message('Welcome to the CaTexT CLI!')

        # set up the modes and initialize them
        super(Basic, self).__init__()
        self.current_mode.set_as_current()

        cfg.cli_logger.debug('... Basic CLI initialized')

    def flash_message(self, message):
        self.show('\n')
        self.show('*------------------------------*')
        self.show('|{:^30}|'.format(message))
        self.show('*------------------------------*')
        self.show('\n\n\n')

    def show(self, *args, newline=True):
        if len(args):
            message = ' '.join(args)
            if newline:
                message = '{}\n'.format(message)
            sys.stderr.write(message)
            sys.stderr.flush()

    def change_mode(self, mode, *args):
        cfg.cli_logger.debug('CLI changing mode (to {})'.format(mode))

        self.flash_message('entering {}'.format(mode))

        if mode not in self.modes:
            if mode == 'lobby':
                self.modes[mode] = Lobby(mode)
            elif 'play' in mode:
                self.modes[mode] = Play(mode)
        self.current_mode = self.modes[mode].set_as_current(*args)

    def set_banner(self, string):
        cfg.cli_logger.debug('CLI setting the current win_banner')
        self.show(string)

    def add_main(self, string):
        cfg.cli_logger.debug('CLI adding a line to the current win_main')
        self.show(string)

    def set_status(self, string):
        cfg.cli_logger.debug('CLI setting current win_status')
        self.show(string)

    def readline(self):
        try:
            line = sys.stdin.readline()
            if line:
                return line.strip('\n')
        except KeyboardInterrupt:
            pass

        self.show('\nNo more input to parse, quitting CaTexT\n\n')
        return None

    def input(self, prompt='', visible=True, completions=None):
        cfg.cli_logger.debug('CLI prompting the user for input')
        if visible:
            self.show(prompt, newline=False)
            line = self.readline()
            if line is None:
                cfg.app.quit()
            else:
                return line
        else:
            return getpass.getpass(prompt)

    def wait(self):
        cfg.cli_logger.debug('CLI waiting')
        self.show('Press <Enter> to continue ... ', newline=False)
        self.readline()

    def quit(self):
        cfg.cli_logger.debug('CLI quitting')


class CLIError(Exception): pass
