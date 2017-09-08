import sys
import pygame
from time import sleep
from random import randint

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

def check_events(ai_settings, screen, stats, scoreboard, play_button, ship, aliens, bullets, alien_bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_event(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, scoreboard, play_button, ship,  aliens, bullets, alien_bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, scoreboard, play_button, ship, aliens, bullets, alien_bullets, mouse_x, mouse_y):
    if play_button.rect.collidepoint(mouse_x, mouse_y) and not stats.game_active:

        pygame.mouse.set_visible(False)
        # 重置游戏
        ai_settings.initialize_dynamic_setting()
        stats.reset_stats()
        stats.game_active = True

        stats.reset_stats()
        scoreboard.prep_score()
        scoreboard.prep_high_score()
        scoreboard.prep_ships()

        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, screen, aliens, alien_bullets)
        ship.center_ship()

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

def update_aliens(ai_settings, stats, scoreboard, screen, ship, aliens, bullets, alien_bullets, time_passed):
    aliens.update()

    check_fleet_edges(aliens)
    # 飞船与敌机碰撞

    for alien in aliens.copy():
        if alien.rect.collidepoint((ship.centerX, ship.centerY)):
            aliens.remove(alien)
            ship_hit(stats, scoreboard, ship, bullets)

    for a_bullet in alien_bullets.copy():
        if a_bullet.rect.collidepoint((ship.centerX, ship.centerY)):
            alien_bullets.remove(a_bullet)
            ship_hit(stats, scoreboard, ship, bullets)

    if ai_settings.decrease_time(time_passed) == True:
        create_fleet(ai_settings, screen, aliens, alien_bullets)

    # 随时间增长，增加难度
    ai_settings.level_up(stats.get_game_time())
    # if len(aliens) < 2 :
    #     ai_settings.level_up()
    #     create_fleet(ai_settings, screen, aliens, alien_bullets)

def update_bullets(ai_settings, screen, stats, scoreboard, aliens, bullets, alien_bullets):
    bullets.update()
    alien_bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)


    for a_bullet in alien_bullets.copy():
        if a_bullet.rect.bottom <= 0:
            alien_bullets.remove(a_bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, scoreboard, aliens, bullets, alien_bullets)

# 处理碰撞
def check_bullet_alien_collisions(ai_settings, screen, stats, scoreboard, aliens, bullets, alien_bullets):

    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for bullet, alien in collisions.items():
            for a in alien:
                stats.score += a.score

        scoreboard.prep_score()
        check_high_score(stats, scoreboard)

    if len(aliens) == 0:
        create_fleet(ai_settings, screen, aliens, alien_bullets)

# 生成敌机
def create_fleet(ai_settings, screen, aliens, alien_bullets):

    aliens_num = int(randint(ai_settings.alien_num_min, ai_settings.alien_num_min + 3))
    x = 0

    for i in range(1, aliens_num):
        alien = Alien(ai_settings, screen, alien_bullets)
        x += alien.rect.width + 5
        alien.resetPos(x)

        aliens.add(alien)

def update_screen(ai_setting, screen, stats, scoreboard, ship, aliens, bullets, alien_bullets, play_button, time_passed):

    scoreboard.show_score()

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    for a_bullet in alien_bullets.sprites():
        a_bullet.draw_bullet()

    ship.blitme(time_passed)

    for alien in aliens.sprites():
        alien.blitme(time_passed, stats)

    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()

# 敌机到达下边缘后销毁
def check_fleet_edges(aliens):
    for alien in aliens.sprites().copy():
        if alien.check_edges('bottom'):
            aliens.remove(alien)
            break

# 撞机
def ship_hit(stats, scoreboard, ship, bullets):

    # 无敌状态
    if ship.check_invincible():
        return False

    stats.ships_left -= 1  # 扣生命数
    play_music('down')  # 坠机音乐

    scoreboard.prep_ships()

    ship.crash(stats.ships_left)

    if stats.ships_left > 0:
        bullets.empty()         # 清空子弹
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_high_score(stats, scoreboard):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        scoreboard.prep_high_score()

# def change_fleet_direction(ai_settings, aliens):#