
import pygame
from pygame.sprite import Sprite


from settings import Settings
from ship import Ship


class Bullet(Sprite):
    """ Class to manage bullets fired from the ship """

    def __init__(self, ai_settings: Settings, screen, ship: Ship):
        """ Create bullet object at ship's current location """
        super().__init__()
        self.screen = screen

        # Create bullet rect at (0,0) and then set correct position
        self.rect = pygame.Rect(
            0, 0, ai_settings.bullet_width, ai_settings.bullet_height)

        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # store the bullets postion as decimal
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed = ai_settings.bullet_speed

    def update(self):
        """Move the bullet up the screen"""

        # Update the decimal value of bullet
        self.y -= self.speed

        # Update the rect postion
        """ rect is responsible for the movement of the object """
        self.rect.y = self.y

    def draw_bullet(self):
        """ Draw the bullet on the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
