import pygame as py
from pygame.sprite import Group


import game_functions as gf
from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    py.init()

    ai_settings = Settings()

    screen = py.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    py.display.set_caption("Alien Invasion!")

    # make play button
    play_button = Button(screen, ai_settings, "Play")

    # make a ship
    ship = Ship(ai_settings, screen)

    # create game stats instance
    stats = GameStats(ai_settings)
    # scoreboard instance
    sb = Scoreboard(screen, ai_settings, stats)

    # make a group to store bullets and aliens
    bullets = Group()
    aliens = Group()

    # Create alien fleet
    gf.create_fleet(ai_settings, screen, aliens, ship)

    while (1):

        gf.check_events(ai_settings, screen, ship, bullets,
                        stats, play_button, aliens, sb)

        if stats.game_active:
            ship.update()
            gf.bullet_update(bullets, aliens, ai_settings,
                             screen, ship, stats, sb)
            gf.update_aliens(aliens, ai_settings, ship,
                             stats, bullets, screen, sb)

        gf.update_screen(screen, ai_settings, ship, bullets,
                         aliens, stats, play_button, sb)


run_game()
