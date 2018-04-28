import curses
from time import sleep
import sys
import random

class CLI():
    def __init__(self, root_logger, env):

        # keep references to root logger and env manager
        self.logger = root_logger
        self.logger.debug('CLI initializing ...')
        self.env = env

        # set up curses screen
        self.stdscr = curses.initscr()
        self.stdscr.keypad(True)
        self.stdscr.refresh()
        curses.noecho()
        curses.cbreak()

        # use "mode"s to logically separate widget/data structure collections
        self.modes = {
            'home'  : Mode('home',  self.logger, ''),
            'lobby' : Mode('lobby', self.logger, 'You are now in the CaTexT lobby'),
            'play'  : Mode('play',  self.logger, 'You are now playing a game of CaTexT')
        }
        self.change_mode('home')

        self.logger.debug('... CLI initialized')

    def change_mode(self, mode):
        self.current_mode = self.modes[mode].set_as_current()

    def set(self, strings):
        self.current_mode.win_main.set(strings)

    def add(self, string):
        self.current_mode.win_main.add(string)

    def status(self, status):
        self.current_mode.win_status.set(status)

    def input(self, prompt, visible=True, completions=None):
        return self.current_mode.win_input.listen(prompt=prompt, visible=visible, completions=completions)

    def wait(self):
        self.current_mode.win_input.wait()

    def quit(self):
        ''' wrapper for cleaning up our curses mode '''
        self.stdscr.keypad(False)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

class Mode():
    def __init__(self, name, logger, default_status):

        self.name = name
        self.logger = logger

        banner_text = '<< CaTexT : {} >>'.format(self.name)
        banner_pad  = int((curses.COLS - len(banner_text))/2) - 1
        self.banner_text = '{}{}'.format(' '*banner_pad, banner_text)

        self.default_status = default_status

        self.win_banner = StripWindow(self.logger, y=0)
        SeparatorWindow(self.logger, y=1)
        self.win_main = ScrollWindow(self.logger, y=2, height=curses.LINES-5)
        SeparatorWindow(self.logger, y=curses.LINES-3)
        self.win_status = StripWindow(self.logger, y=curses.LINES-2)
        self.win_input = InputWindow(self.logger, y=curses.LINES-1)

        self.win_input.bind_to_scrollwindow(self.win_main)

    def set_as_current(self):

        self.win_banner.set(self.banner_text)
        self.win_status.set(self.default_status)
        self.win_input.set('')

        return self

class Window():
    def __init__(self, logger, dimensions, prefix=''):

        # keep the same logger
        self.logger = logger

        # get dimensions of the strip for our newwin()
        self.height, self.width, self.start_y, self.start_x = dimensions
        self.logger.debug(str(dimensions))
        self.win = curses.newwin(self.height, self.width, self.start_y, self.start_x)
        self.win.keypad(True)

        # save this prefix
        self.prefix = prefix

class StripWindow(Window):
    def __init__(self, logger, y=-1, prefix=''):
        super().__init__(logger, (1, curses.COLS, y, 0), prefix=prefix)

        # variable string
        self.str_var = ''
        self.str_start = 0
        self.str_width = self.width - len(self.prefix)

        self.set('')

    def set(self, string, reset=False):
        self.str_var = str(string)
        self.str_start = 0 if reset else self.str_start
        self.refresh()

    def refresh(self):
        visible_str_var = self.str_var[self.str_start:self.str_start+self.str_width]
        visible_str = escape('{}{}'.format(self.prefix, visible_str_var))
        self.logger.debug(visible_str)
        #self.logger.debug(type(self.win).addstr)
        self.win.addstr(0, 0, visible_str)
        self.win.clrtoeol()
        self.win.refresh()

class SeparatorWindow(StripWindow):
    def __init__(self, logger, y=-1):
        super().__init__(logger, y=y)
        self.set('-'*(curses.COLS-1))

class InputWindow(StripWindow):
    def __init__(self, logger, y=-1, prefix=''):
        self.default_prompt = ' > '
        super().__init__(logger, y=y, prefix=self.default_prompt)
        self.set_prompt()

    def set_prompt(self, prompt=None):
        self.logger.debug('new prompt: {}'.format(prompt))
        self.prefix = self.default_prompt if prompt is None else prompt

        self.str_var = ''
        self.str_start = 0
        self.str_width = self.width - len(self.prefix)

        self.refresh()

    def bind_to_scrollwindow(self, scrollwindow):
        self.sw = scrollwindow

    def listen(self, prompt='', visible=True, completions=None):

        self.set_prompt(prompt)

        string = ''
        while True:
            key = self.win.getkey()
            num = ord(key) if len(key)==1 else -1
            self.logger.debug('pressed "{}" ({})'.format(key, num))

            if num == 10: # <Enter>
                return string
            elif num == 27: # <Esc>
                pass
            elif num == 127: # <Backspace>
                if len(string):
                    y, x = self.win.getyx()
                    self.win.delch(y, x-1)
                    string = string[:-1]
                self.win.refresh()
            elif key == 'KEY_UP':
                self.sw.scroll_up()
            elif key == 'KEY_DOWN':
                self.sw.scroll_down()
            elif key == 'KEY_LEFT':
                pass
            elif key == 'KEY_RIGHT':
                pass
            else: # regular key
                string += key
                self.win.addstr(key if visible else '*')
                self.win.refresh()

    def wait(self):
        self.logger.debug('waiting')
        self.set_prompt(prompt='   press any key to continue ... ')
        self.win.getch()

class ScrollWindow(Window):
    def __init__(self, logger, y=-1, height=-1):
        super().__init__(logger, (height, curses.COLS, y, 0))

        # variable string array
        self.all_strings = []
        self.filtered_strings = []
        self.string_filter_all = ['game', 'message', 'server', '<NONE>']
        self.string_filter = self.string_filter_all
        self.start_line = 0

    def scroll_up(self):
        if self.start_line > 0:
            self.start_line -= 1
            self.refresh()

    def scroll_down(self):
        if len(self.filtered_strings) > self.start_line + self.height:
            self.start_line += 1
            self.refresh()

    def refresh(self):
        #self.logger.debug(self.all_strings)
        #self.logger.debug(self.filtered_strings)
        for line_num in range(self.height):
            id = self.start_line + line_num
            string = self.filtered_strings[id].string if id < len(self.filtered_strings) else ''
            string = escape(string)
            if line_num == 0 and self.start_line > 0:
                self.logger.debug('scroll up')
                string = ' <Up>'
            if line_num == self.height-1 and len(self.filtered_strings) - 1 > id:
                self.logger.debug('start_line {}, line_num {}, id {}, height {}, len-strings {}'.format(self.start_line, line_num, id, self.height, len(self.filtered_strings)))
                self.logger.debug('scroll down')
                string = ' <Down>'
            #self.logger.debug(string)
            self.win.addstr(line_num, 0, string)
            self.win.clrtoeol()
        self.win.refresh()

    def set(self, strings, label='server'):
        for string in strings:
            string = ScrollString(string, len(self.all_strings), label)
            self.all_strings.append(string)
        self.filter_strings(self.string_filter)
        self.refresh()

    def add(self, string, label='<NONE>'):
        string = ScrollString(string, len(self.all_strings), label)
        self.all_strings.append(string)
        self.filter_strings(self.string_filter)
        self.refresh()

    def filter_strings(self, filter=None):
        self.string_filter = self.string_filter_all if filter is None else filter
        self.filtered_strings = [string for string in self.all_strings if string.is_in_filter(filter)]

class ScrollString():
    def __init__(self, string, id, label):

        # save this stuff
        self.string = string
        self.id = id
        self.label = label

    def is_in_filter(self, filter):
        return self.label in filter

def escape(string):
    return string[:curses.COLS]

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
