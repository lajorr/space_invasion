import pygame
from pygame.sprite import Sprite

from settings import Settings


class Alien(Sprite):
    def __init__(self, screen, ai_settings: Settings) -> None:
        ''' Initialize the alien and set its starting position '''
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # load the alien image and get its rect
        self.image = pygame.image.load('images/alien.png')
        self.rect = self.image.get_rect()

        # repostion it to top left
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store exact postion of alien
        self.x = float(self.rect.x)

    # def blitme(self):
    #     """ Draw the alien at its current location """
    #     self.screen.blit(self.image, self.rect)

    def check_edge(self):
        """ checks if the fleet has hit an edge """
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """ Move alien left or right """
        self.x += (self.ai_settings.alien_speed *
                   self.ai_settings.fleet_direction)

        self.rect.x = self.x
