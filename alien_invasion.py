import pygame
from pygame.sprite import Group

from button import Button
from game_stats import GameStats
from settings import Settings
from ship import Ship
from scoreboard import Scoreboard
import game_funcitons as gf

def run_game():
    pygame.init()
    pygame.mixer.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))

    pygame.display.set_caption("Alien Invasion")
    play_button = Button(ai_settings, screen, 'PLAY')

    stats      = GameStats(ai_settings)
    scoreboard = Scoreboard(ai_settings, screen, stats)
    bg_img1 = pygame.image.load("images/map.jpg").convert()
    bg_img2 = bg_img1.copy()
    pos_y1  = -1024
    pos_y2  = 0

    ship    = Ship(ai_settings, screen)
    aliens  = Group()
    bullets = Group()
    alien_bullets = Group()

    gf.create_fleet(ai_settings, screen, aliens, alien_bullets)

    #背景音乐
    gf.play_music('bgm')

    clock = pygame.time.Clock()

    while True:
        # 按键事件
        gf.check_events(ai_settings, screen, stats, scoreboard, play_button, ship, aliens, bullets, alien_bullets)
        gf.update_bullets(ai_settings, screen, stats, scoreboard, aliens, bullets, alien_bullets)

        time_passed = clock.tick()

        if stats.game_active:
            stats.increase_time(time_passed)
            # 飞机/子弹 更新
            ship.update()
            #敌机位置
            gf.update_aliens(ai_settings, stats, scoreboard, screen, ship, aliens, bullets, alien_bullets, time_passed)

        # 背景滚动
        screen.blit(bg_img1, (0, pos_y1))
        screen.blit(bg_img2, (0, pos_y2))

        pos_y1 += ai_settings.bg_roll_speed_factor
        pos_y2 += ai_settings.bg_roll_speed_factor

        if pos_y1 > 0:
            pos_y1 = -1024
        if pos_y2 > 1024:
            pos_y2 = 0

        gf.update_screen(ai_settings, screen, stats, scoreboard, ship, aliens, bullets, alien_bullets, play_button, time_passed)

run_game()