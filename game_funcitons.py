import sys
import pygame

from bullet import Bullet

def check_keydown_event(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_d:
        ship.moving_right = True
    elif event.key == pygame.K_a:
        ship.moving_left = True
    elif event.key == pygame.K_s:
        ship.moving_down = True
    elif event.key == pygame.K_w:
        ship.moving_up = True
    elif event.key == pygame.K_j and len(bullets) < ai_settings.bullets_allowed:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_ESCAPE:
        sys.exit()

# biu biu biu
def fire_bullet(ai_settings, screen, ship, bullets):
    new_bullet = Bullet(ai_settings, screen, ship)
    bullets.add(new_bullet)

def check_keyup_event(event, ship):
    if event.key == pygame.K_d:
        ship.moving_right = False
    if event.key == pygame.K_a:
        ship.moving_left = False
    if event.key == pygame.K_s:
        ship.moving_down = False
    if event.key == pygame.K_w:
        ship.moving_up   = False

def check_events(ai_settings, screen, ship, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_event(event, ship)

def update_bullets(bullets):
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)


def update_screen(ai_setting, screen, ship, bullets):

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    pygame.display.flip()