import pygame.font
from pygame.surface import Surface

from settings import Settings
from game_stats import GameStats


class Scoreboard():
    """ Class to show scoring system """

    def __init__(self, screen: Surface, ai_settings: Settings, stats: GameStats) -> None:
        """ Initializing Score keeping attributes """
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.ai_settings = ai_settings
        self.stats = stats

        # Font Settings
        self.color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score image
        self.prep_score()
        self.prep_high_score()

    def prep_high_score(self):
        """ turn highscore to image """
        high_score = int(round(self.stats.score, -1))
        high_score_str = "{:,}".format(high_score)

        self.high_score_image = self.font.render(
            high_score_str, True, self.color, self.ai_settings.bg_color)

        # Reposition to Top Center
        self.hs_rect = self.high_score_image.get_rect()
        self.hs_rect.centerx = self.screen_rect.centerx
        self.hs_rect.top = self.score_rect.top

    def prep_score(self):
        """ Turn text to image"""

        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(
            score_str, True, self.color, self.ai_settings.bg_color)

        # Display score at top right
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """ Draw Score to the screen """
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.hs_rect)
