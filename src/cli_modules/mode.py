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

    def get_players_string(self, game):
        if game['status'] == 'in-progress':
            return '{:2}'.format(len(game['players']))
        elif game['status'] == 'ready':
            return '{:2}'.format(len(game['players']))
        elif game['status'] == 'pending':
            return '{:2}/{:2}'.format(len(game['players']), game['settings']['numHumans'])

    def check_if_user_in_game(self, game):
        user = cfg.current_user

        for player in game['players']:
            cfg.cli_logger.debug('"{}" "{}"'.format(player['name'], user.name))
            if player['name'] == user.name:
                cfg.cli_logger.debug('same')
                return True

        return False

    def print_games(self, games):

        split_games = { 'top':[], 'middle':[], 'bottom':[] }
        for game in games:

            user_in_game = self.check_if_user_in_game(game)
            cfg.cli_logger.debug('{} {}'.format(user_in_game, game['status']))
            if game['status'] == 'in-progress':
                if user_in_game:
                    split_games['top'].append(game)
            else:
                if user_in_game:
                    split_games['middle'].append(game)
                elif not(game['isFull']):
                    split_games['bottom'].append(game)

        self.win_main.add('IN-PROGRESS')
        self.print_game_list(split_games['top'], 1)
        self.win_main.add('')
        self.win_main.add('PENDING')
        self.print_game_list(split_games['middle'], len(split_games['top']))
        self.win_main.add('')
        self.win_main.add('AVAILABLE')
        self.print_game_list(split_games['bottom'], len(split_games['top'])+len(split_games['middle']))

    def print_game_list(self, games, start_at=1):

        self.win_main.add('  num    id         author      players      last updated')
        self.win_main.add(' ---- -------- ---------------- ------- ----------------------')
        for i, game in enumerate(games):
            gamestring = ' {:3}) {:8} {:^16} {:^7} {:<22}'.format(start_at+i
                , game['id'][-8:]
                , game['author']['name']
                , self.get_players_string(game)
                , game['updated'] )
            self.win_main.add(gamestring)

    def set_as_current(self, args):

        cfg.cli_logger.debug('Lobby is now the current mode')

        self.win_banner.set(self.get_banner_text())
        self.win_main.set([])
        self.win_status.set('')
        self.win_input.set('')

        self.print_games(args['games'])

        return self

class Play(Mode):
    def set_as_current(self, *args):

        cfg.cli_logger.debug('Play ({}) is now the current mode'.format(self.name))

        self.win_banner.set(self.get_banner_text())
        self.win_main.set([])
        self.win_status.set('')
        self.win_input.set('')

        return self
