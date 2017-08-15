import sys
import pygame
from time import sleep

from bullet import Bullet
from alien import Alien

# 监听按键按下事件
def check_keydown_event(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_d:
        ship.moving_right = True
        ship.set_image('right')
    elif event.key == pygame.K_a:
        ship.moving_left = True
        ship.set_image('left')
    elif event.key == pygame.K_s:
        ship.moving_down = True
        ship.set_image('down')
    elif event.key == pygame.K_w:
        ship.moving_up = True
        ship.set_image('up')
    elif event.key == pygame.K_j and len(bullets) < ai_settings.bullets_allowed:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_ESCAPE:
        sys.exit()

# biu biu biu
def fire_bullet(ai_settings, screen, ship, bullets):
    new_bullet = Bullet(ai_settings, screen, ship)
    play_music('fire')
    bullets.add(new_bullet)

# 监听按键松开事件
def check_keyup_event(event, ship):
    if event.key == pygame.K_d:
        ship.moving_right = False
        ship.set_image('stop')
    if event.key == pygame.K_a:
        ship.moving_left = False
        ship.set_image('stop')
    if event.key == pygame.K_s:
        ship.moving_down = False
        ship.set_image('stop')
    if event.key == pygame.K_w:
        ship.moving_up   = False
        ship.set_image('stop')

def check_events(ai_settings, screen, stats, play_button, ship, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_event(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y)

def check_play_button(stats, play_button, mouse_x, mouse_y):
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        stats.game_active = True

def play_music(type):

    if type == "bgm":
        pygame.mixer.music.load("sounds/bg_music.mp3")
        pygame.mixer.music.play(-1)
    elif type == "fire":
        effect = pygame.mixer.Sound('sounds/fire.wav')
        pygame.mixer.Sound.play(effect)
    elif type == "down":
        effect = pygame.mixer.Sound('sounds/user_down.wav')
        pygame.mixer.Sound.play(effect)

def update_aliens(stats, screen, ship, aliens, bullets):
    aliens.update()

    check_fleet_edges(aliens)
    # 飞船与敌机碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(stats, ship, bullets)

def update_bullets(ai_settings, screen, aliens, bullets):
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, aliens, bullets)

# 处理碰撞
def check_bullet_alien_collisions(ai_settings, screen, aliens, bullets):

    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if len(aliens) == 0:
        create_fleet(ai_settings, screen, aliens)

# 生成敌机
def create_fleet(ai_settings, screen, aliens):
    alien = Alien(ai_settings, screen)
    aliens.add(alien)

def update_screen(ai_setting, screen, stats, ship, aliens, bullets, play_button):

    if not stats.game_active:
        play_button.draw_button()

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)
    pygame.display.flip()

def check_fleet_edges(aliens):
    for alien in aliens.sprites().copy():
        if alien.check_edges('bottom'):
            aliens.remove(alien)
            break

# 撞机
def ship_hit(stats, ship, bullets):

    stats.ships_left -= 1  # 扣生命数
    play_music('down')  # 坠机音乐

    if stats.ships_left > 0:
        bullets.empty()         # 清空子弹
        ship.center_ship()      # 重置位置
        sleep(0.5)              # 睡一会
    else:
        stats.game_active = False




# def change_fleet_direction(ai_settings, aliens):#