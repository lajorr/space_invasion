import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        """ init ship and its starting pos """

        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        # load the ship image and get its rect
        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # start each new ship ant bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # store a decimal number for ship's center
        self.center = float(self.rect.centerx)

        # movement flag
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        """ Draw the ship at its current location """
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """ Centers the ship"""
        self.center = self.screen_rect.centerx

    def update(self):
        """Update the ship's position based on movement flag"""

        """ since self.rect.centerx only takes integer value and the ship_speed is a floating point
        we first store it in self.center and later assign it to self.rect     
        """

        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed

        # Update the rect object from center
        self.rect.centerx = self.center
