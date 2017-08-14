import pygame
from pygame.sprite import Group

from button import Button
from game_stats import GameStats
from settings import Settings
from ship import Ship
import game_funcitons as gf

def run_game():
    pygame.init()
    pygame.mixer.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))

    pygame.display.set_caption("Alien Invasion")
    play_button = Button(ai_settings, screen, 'PLAY')

    stats   = GameStats(ai_settings)

    bg_img1 = pygame.image.load("images/map.jpg").convert()
    bg_img2 = bg_img1.copy()
    pos_y1  = -1024
    pos_y2  = 0

    ship    = Ship(ai_settings, screen)
    aliens  = Group()
    bullets = Group()

    gf.create_fleet(ai_settings, screen, aliens)

    #背景音乐
    gf.play_music('bgm')


    while True:
        # 按键事件
        gf.check_events(ai_settings, screen, stats, play_button, ship, bullets)

        if stats.game_active:
            # 飞机/子弹 更新
            ship.update()
            gf.update_bullets(ai_settings, screen, aliens, bullets)

            #敌机位置
            gf.update_aliens(stats, screen, ship, aliens, bullets)

        # 背景滚动
        screen.blit(bg_img1, (0, pos_y1))
        screen.blit(bg_img2, (0, pos_y2))

        pos_y1 += ai_settings.bg_roll_speed_factor
        pos_y2 += ai_settings.bg_roll_speed_factor

        if pos_y1 > 0:
            pos_y1 = -1024
        if pos_y2 > 1024:
            pos_y2 = 0

        gf.update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button)

run_game()