import sys
import pygame
from pygame.sprite import Group
from time import sleep

from ship import Ship
from bullet import Bullet
from settings import Settings
from alien import Alien
from game_stats import GameStats
from button import Button


def check_events(ai_settings, screen, ship: Ship, bullets, stats, play_button, aliens, sb):
    """ responds to any keyboard or mouse events """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ship, ai_settings,
                                 screen, bullets, stats, aliens, sb)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x,
                              mouse_y, aliens, bullets, ai_settings, screen, ship, sb)


def check_play_button(stats, play_button: Button, mouse_x, mouse_y, aliens, bullets, ai_settings, screen, ship, sb):
    """ Start a new game when clicked play """
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)

    if button_clicked:
        start_game(stats, aliens, bullets, ai_settings, screen, ship, sb)


def start_game(stats, aliens, bullets, ai_settings, screen, ship, sb):

    if not stats.game_active:

        # Reset Game Speed setting
        ai_settings.initialize_dynamic_settings()

        # hide mouse cursor
        pygame.mouse.set_visible(False)

        stats.game_active = True
        # reset game stats
        stats.reset_stats()
        sb.prep_score()
        sb.prep_level()
        sb.prep_ships()
        reset_game(aliens, bullets, ai_settings, screen, ship, stats, sb)


def reset_game(aliens: Group, bullets: Group, ai_settings, screen, ship, stats, sb):

    # empty the list of aliens and bullets
    aliens.empty()
    bullets.empty()
    # create a new fleet and center the ship
    create_fleet(ai_settings, screen, aliens, ship)
    ship.center_ship()


def check_keydown_events(event, ship, ai_settings: Settings, screen, bullets, stats, aliens, sb):
    """ Respond to Keydown """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(bullets, ai_settings, screen, ship)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_p:
        start_game(stats, aliens, bullets, ai_settings, screen, ship, sb)


def check_keyup_events(event, ship):
    """ Respond to key release """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_screen(screen, ai_settings: Settings, ship, bullets: Group, aliens, stats: GameStats, play_button, sb):
    """Update images on the screen and flip to the new screen."""
    # redraw screen during each iteration of loop
    screen.fill(ai_settings.bg_color)

    # redraw all bullets behind ship and aliens\
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    # Draw Score info
    sb.show_score()

    # Draw the play button if game is inactive
    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()


def bullet_update(bullets, aliens, ai_settings, screen, ship, stats, sb):
    """update position of bullets and get rid of old bullets"""
    # Update Bullet position
    bullets.update()
    # get rid of bullets that have dissapeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collision(
        bullets, aliens, ai_settings, screen, ship, stats, sb)


def check_bullet_alien_collision(bullets, aliens, ai_settings, screen, ship, stats, sb):
    """ check for bullet and alien collision"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    # the True value is for whether to delete the bullet and alien respectively or not
    # For high power bullet that destroys all alinds in its path we can set bullet delete ( first one ) to false

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)

            sb.prep_score()

        check_high_score(stats, sb)
    if len(aliens) == 0:
        # Destroy all bullets and spawn new alien fleet
        bullets.empty()
        ai_settings.increase_speed()

        # increase level
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, aliens, ship)


def fire_bullets(bullets, ai_settings, screen, ship):
    """ Create new bullet and add it to bullets group"""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_of_aliens_x(ai_settings, alien_width):
    """ to get number of aliens in a row """
    available_space_x = ai_settings.screen_width - (2 * alien_width)
    number_of_aliens_x = int(available_space_x / (2*alien_width))
    return number_of_aliens_x


def get_number_row(ai_settings, ship_height, alien_height):
    """ Determine the number of rows of aliens """

    available_space_y = ai_settings.screen_height - \
        (3*alien_height) - ship_height

    number_rows = int(available_space_y / (2*alien_height))
    return number_rows


def create_alien(screen, ai_settings, aliens, alien_number, row_number):
    """ Create and return an alien """
    alien = Alien(screen, ai_settings)
    alien_width = alien.rect.width

    alien.x = alien_width + 2 * alien_width * alien_number

    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2*alien.rect.height * row_number

    aliens.add(alien)


def create_fleet(ai_settings: Settings, screen, aliens: Group, ship):
    """ Create a full fleet of aliens """
    # Create an alien and find the number of aliens in a row
    # spacing between aliens is 1 alien
    alien = Alien(screen, ai_settings)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    ship_height = ship.rect.height

    number_of_aliens_x = get_number_of_aliens_x(ai_settings, alien_width)
    number_rows = get_number_row(
        ai_settings, ship_height, alien_height)

    for row_number in range(number_rows):
        # Create the first row of aliens
        for alien_number in range(number_of_aliens_x):
            # Create an alien and place it in row
            create_alien(screen, ai_settings, aliens, alien_number, row_number)


def check_fleet_edge(ai_settings, aliens):
    """ responds appropriately if any alien and reached an edge """
    for alien in aliens.sprites():
        if alien.check_edge():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """ Drop the fleet and change direction """
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(aliens, ai_settings, ship: Ship, stats, bullets, screen, sb):
    """ update the positions of all aliens """
    check_fleet_edge(ai_settings, aliens)
    aliens.update()

    # alien- ship collision
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(stats, aliens, bullets, ai_settings, screen, ship, sb)

    # if alien hit the bottom
    check_alien_bottom(screen, aliens, stats, bullets, ai_settings, ship, sb)


def ship_hit(stats: GameStats, aliens: Group, bullets: Group, ai_settings, screen, ship, sb):
    """Responds to ship being hit by alien"""

    if stats.ships_left > 0:
        # reduce 1 li   fe/ ship
        stats.ships_left -= 1

        #update scoreboard
        sb.prep_ships()

        # empty the list of aliends and bullets
        reset_game(aliens, bullets, ai_settings, screen, ship, stats, sb)

        # pause -- to let user realise they've been hit
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_alien_bottom(screen, aliens, stats, bullets, ai_settings, ship, sb):
    """ Checks if aliens hit the bottom of the screen """
    screen_rect = screen.get_rect()

    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            """ we need the same responseas ship hit"""
            ship_hit(stats, aliens, bullets, ai_settings, screen, ship, sb)
            break


def check_high_score(stats: GameStats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
