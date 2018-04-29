import curses
import os

import config as cfg

from window import StripWindow, SeparatorWindow, InputWindow, ScrollWindow



class Mode():
    def __init__(self, name):

        cfg.cli_logger.debug('initializing Mode (name={})'.format(name))

        self.name = name

        self.win_banner = StripWindow(y=0)
        SeparatorWindow(y=1)
        self.win_main = ScrollWindow(y=2, height=curses.LINES-5)
        SeparatorWindow(y=curses.LINES-3)
        self.win_status = StripWindow(y=curses.LINES-2)
        self.win_input = InputWindow(y=curses.LINES-1)

        self.win_input.bind_to_scrollwindow(self.win_main)

    def get_banner_text(self):

        current_user = cfg.env.get('CURRENT_USER', None)

        if current_user is '':

            banner_text = '<< CaTexT : {} >>'.format(self.name)
            banner_pad  = int((curses.COLS - len(banner_text))/2) - 1
            banner_text = '{}{}'.format(' '*banner_pad, banner_text)

        else:

            left_banner = ' CaTexT ({})'.format(self.name)
            right_banner= 'logged in as {}'.format(current_user)
            banner_pad = curses.COLS - len(left_banner) - len(right_banner) - 1
            banner_text = '{}{}{}'.format(left_banner, ' '*banner_pad, right_banner)

        cfg.cli_logger.debug('Mode banner text : "{}"'.format(banner_text))

        return banner_text



class Home(Mode):
    def set_as_current(self, *args):

        cfg.cli_logger.debug('Home is now the current mode')

        lines = ['','   Welcome to CaTexT','']
        users = os.listdir(cfg.env.get('USERS_ROOT'))
        if len(users):
            lines.append('SAVED LOGINS:')
            lines += [' - {}'.format(user) for user in users]
        else:
            lines.append('NO SAVED LOGINS')

        self.win_banner.set(self.get_banner_text())
        self.win_main.set(lines)
        self.win_status.set('Log in with your CatOnline credentials')
        self.win_input.set('')

        return self

class Lobby(Mode):
    def set_as_current(self, *args):

        cfg.cli_logger.debug('Lobby is now the current mode')

        self.win_banner.set(self.get_banner_text())
        self.win_main.set([])
        self.win_status.set('')
        self.win_input.set('')

        return self

class Play(Mode):
    def set_as_current(self, *args):

        cfg.cli_logger.debug('Play ({}) is now the current mode'.format(self.name))

        self.win_banner.set(self.get_banner_text())
        self.win_main.set([])
        self.win_status.set('')
        self.win_input.set('')

        return self
