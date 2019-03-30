from print_util import pprint


class CLI(object):
    @staticmethod
    def intro():
        intro_key = {'1': 'view_current_member',
                     '2': 'input_clan_war_member',
                     '3': 'show_filtered_member'}
        pprint('===== Clash Royale Clan Member Manager =====')
        pprint('|1. View current member                    |')
        pprint('|2. Input member who attended clan war day |')
        pprint('|3. Show filtered member                   |')
        pprint('============================================')

cli = CLI()

