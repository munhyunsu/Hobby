class Referee(object):
    def go(self, home, away):
        home_input = home.get_hands()
        away_input = away.get_hands()
        if away_input == '가위':
            if home_input == '가위':
                home.round_draw()
                away.round_draw()
            elif home_input == '바위':
                home.round_win()
                away.round_lose()
            elif home_input == '보':
                home.round_lose()
                away.round_win()
        elif away_input == '바위':
            if home_input == '가위':
                home.round_lose()
                away.round_win()
            elif home_input == '바위':
                home.round_draw()
                away.round_draw()
            elif home_input == '보':
                home.round_win()
                away.round_lose()
        elif away_input == '보':
            if home_input == '가위':
                home.round_win()
                away.round_lose()
            elif home_input == '바위':
                home.round_lose()
                away.round_win()
            elif home_input == '보':
                home.round_draw()
                away.round_draw()
