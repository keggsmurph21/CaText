import os

import config as cfg

__all__ = ['Home', 'Lobby', 'Play']

class Mode(object):
    def __init__(self, name):

        cfg.cli_logger.debug('initializing Mode (name={})'.format(name))

        self.width = cfg.env.get('TERM_WIDTH')
        self.name = name

    def __repr__(self):
        return 'Mode (type={}, name={})'.format(self.__class__.__name__, self.name)

    def get_banner_text(self, *args):

        current_user = cfg.env.get('CURRENT_USER', None)

        if current_user is '':

            banner_text = '<< CaTexT : {} >>'.format(self.name)
            banner_pad  = int((self.width - len(banner_text))/2) - 1
            banner_text = '{}{}'.format(' '*banner_pad, banner_text)

        else:

            left_banner = ' CaTexT ({})'.format(self.name)
            right_banner= 'logged in as {}'.format(current_user)
            banner_pad = self.width - len(left_banner) - len(right_banner) - 1
            banner_text = '{}{}{}'.format(left_banner, ' '*banner_pad, right_banner)

        cfg.cli_logger.debug('Mode banner text : "{}"'.format(banner_text))

        return banner_text

    def get_main_text(self, *args):
        return []

    def get_status_text(self, *args):
        return ''

    def get_input_text(self, *args):
        return ''

    def set_as_current(self, *args):

        cfg.cli_logger.debug('Current mode: {}'.format(self))

        cfg.cli.set_banner(self.get_banner_text())
        cfg.cli.set_main(self.get_main_text(*args))
        cfg.cli.set_status(self.get_status_text())

        return self


class Home(Mode):
    def get_main_text(self):

        lines = ['','   Welcome to CaTexT','']
        users = os.listdir(cfg.env.get('USERS_ROOT'))
        if len(users):
            lines.append('SAVED LOGINS:')
            lines += [' - {}'.format(user) for user in users]
        else:
            lines.append('NO SAVED LOGINS')

        return lines

    def get_status_text(self):
        return 'Log in with your CatOnline credentials'

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
            if player['name'] == user.name:
                return True

        return False

    def print_game_list(self, title='', games=[], count=1, lines=[]):

        if len(games):
            lines.append(title)
            lines.append('  num    id         author      players      last updated')
            lines.append(' ---- -------- ---------------- ------- ----------------------')
            for i, game in enumerate(games):
                gamestring = ' {:3}) {:8} {:^16} {:^7} {:<22}'.format(count
                    , game['id'][-8:]
                    , game['author']['name']
                    , self.get_players_string(game)
                    , game['updated'] )
                lines.append(gamestring)
                count += 1
            lines.append('')

        return count

    def get_main_text(self, args):

        games = args['games']

        split_games = { 'top':[], 'middle':[], 'bottom':[] }
        for game in games:

            user_in_game = self.check_if_user_in_game(game)
            if game['status'] == 'in-progress':
                if user_in_game:
                    split_games['top'].append(game)
            else:
                if user_in_game:
                    split_games['middle'].append(game)
                elif not(game['isFull']):
                    split_games['bottom'].append(game)

        count, lines = 1, []
        count = self.print_game_list(title='IN-PROGRESS', games=split_games['top'], count=count, lines=lines)
        count = self.print_game_list(title='PENDING', games=split_games['middle'], count=count, lines=lines)
        count = self.print_game_list(title='AVAILABLE', games=split_games['bottom'], count=count, lines=lines)

        return lines

class Play(Mode):
    pass
