import curses

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
