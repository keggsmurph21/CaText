import curses
import os

from cli_window import StripWindow, SeparatorWindow, InputWindow, ScrollWindow



class Mode():
    def __init__(self, name, logger, env, get_path):

        # keep references
        self.name = name
        self.logger = logger
        self.env = env
        self.get_path = get_path

        self.win_banner = StripWindow(self.logger, y=0)
        SeparatorWindow(self.logger, y=1)
        self.win_main = ScrollWindow(self.logger, y=2, height=curses.LINES-5)
        SeparatorWindow(self.logger, y=curses.LINES-3)
        self.win_status = StripWindow(self.logger, y=curses.LINES-2)
        self.win_input = InputWindow(self.logger, y=curses.LINES-1)

        self.win_input.bind_to_scrollwindow(self.win_main)

    def get_banner_text(self):

        current_user = self.env.get('CURRENT_USER', None)

        if current_user is '':

            banner_text = '<< CaTexT : {} >>'.format(self.name)
            banner_pad  = int((curses.COLS - len(banner_text))/2) - 1
            banner_text = '{}{}'.format(' '*banner_pad, banner_text)

        else:

            left_banner = ' CaTexT ({})'.format(self.name)
            right_banner= 'logged in as {}'.format(current_user)
            banner_pad = curses.COLS - len(left_banner) - len(right_banner) - 1
            banner_text = '{}{}{}'.format(left_banner, ' '*banner_pad, right_banner)

        return banner_text



class Home(Mode):
    def __init__(self, *args):

        super().__init__(*args)

    def set_as_current(self, *args):

        self.logger.debug('setting <home> as the current mode')

        lines = ['','   << Welcome to CaTexT >>','']
        users = os.listdir(self.get_path('.users'))
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
    def __init__(self, *args):

        super().__init__(*args)

    def set_as_current(self, *args):

        self.logger.debug('setting <lobby> as the current mode')

        self.win_banner.set(self.get_banner_text())
        self.win_main.set([])
        self.win_status.set('')
        self.win_input.set('')

        return self

class Play(Mode):
    def __init__(self, *args):

        super().__init__(*args)

    def set_as_current(self, *args):

        self.logger.debug('settings <{}> as the current mode'.format(self.name))

        self.win_banner.set(self.get_banner_text())
        self.win_main.set([])
        self.win_status.set('')
        self.win_input.set('')

        return self
