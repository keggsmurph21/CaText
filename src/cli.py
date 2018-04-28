import curses
from time import sleep
import sys

class CLI():
    def __init__(self, root_logger, env):

        # keep references to root logger and env manager
        self.logger = root_logger
        self.logger.debug('CLI initializing ...')
        self.env = env

        # set up curses
        self.stdscr = curses.initscr()
        self.stdscr.keypad(True)
        curses.noecho()
        curses.cbreak()

        # title window
        self.title_win = curses.newwin(1, curses.COLS, 0, 0)
        title_text = '<< CaTexT >>'
        self.title_win.addstr(0, center_x(title_text), title_text)
        self.title_win.refresh()

        # abstraction to deal with dialog stuff
        self.dialog = DialogWin(self.logger)

    def quit(self):
        ''' wrapper for cleaning up our curses mode '''
        self.stdscr.keypad(False)
        curses.echo()
        curses.nocbreak()
        curses.endwin()


class DialogWin():
    def __init__(self, logger):

        # keep the same logger
        self.logger = logger

        # set up curses window
        self.win = curses.newwin(curses.LINES-1, curses.COLS, 1, 0)
        self.win.keypad(True)

        # internal track of where we are in the window
        self.current_line = 0

    def print_line(self, str, x=0):
        self.win.addstr(self.current_line, x, str)
        self.current_line += 1
        self.win.refresh()

    def print_lines(self, strings, mark=None):
        for i, string in enumerate(strings):
            if mark is not None:
                if i == mark:
                    str = ' * {}'.format(string)
                else:
                    str = '   {}'.format(string)
            self.print_line(str)

    def prompt_from_list(self, choices, current=0):

        self.logger.debug(str(choices))
        dirty = True
        reset_line = self.current_line

        while True:

            if dirty:
                self.current_line = reset_line
                self.print_lines(choices, mark=current)
                dirty = False

            self.win.move(reset_line+current, 1)
            key = self.win.getkey()
            self.logger.debug('user pressed "{}"'.format(key))
            if key == '\n':
                choice = choices[current]
                self.logger.debug('user selected "{}"'.format(choice))
                self.clear()
                return choice
            elif key == 'KEY_UP':
                current -= 1
                current = current % len(choices)
                dirty = True
            elif key == 'KEY_DOWN':
                current += 1
                current = current % len(choices)
                dirty = True

    def prompt_credentials(self):

        self.print_line('   username: ')
        username = self.prompt_string()
        self.print_line('   password: ')
        password = self.prompt_password()

        self.clear()

        return username, password

    def prompt_string(self):
        string = ''
        while True:
            key = self.win.getkey()
            self.logger.debug('user pressed "{}"'.format(key))
            if key == '\n':
                return string
            elif len(key) > 1:
                pass
            elif ord(key) == 127:
                self.logger.debug('backspace')
                if len(string):
                    y, x = self.win.getyx()
                    self.win.delch(y, x-1)
                    string = string[:-1]
            else:
                string += key
                self.win.addstr(key)
            self.win.refresh()

    def prompt_password(self):
        string = ''
        while True:
            key = self.win.getkey()
            self.logger.debug('user pressed "{}"'.format(key))
            if key == '\n':
                return string
            elif ord(key) == 127:
                self.logger.debug('backspace')
                if len(string):
                    y, x = self.win.getyx()
                    self.win.delch(y, x-1)
                    string = string[:-1]
            else:
                string += key
                self.win.addstr('*')
            self.win.refresh()

    def clear(self):
        self.win.clear()
        self.current_line = 0


def center_x(str):
    return int((curses.COLS - len(str))/2)
