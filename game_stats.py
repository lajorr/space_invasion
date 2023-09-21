from settings import Settings


class GameStats():
    """ Track Statisics for game """

    def __init__(self, ai_settings: Settings) -> None:
        """ initialize stats"""
        self.ai_settings = ai_settings
        self.reset_stats()

        # start game in an inactice state
        self.game_active = False

        # highscore
        self.high_score = 0

    def reset_stats(self):
        """ Initialize statistics that can change during game """
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
