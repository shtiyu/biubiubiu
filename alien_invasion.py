import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
import game_funcitons as gf

def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))

    pygame.display.set_caption("Alien Invasion")

    bg_img1 = pygame.image.load("images/map.jpg").convert()
    bg_img2 = bg_img1.copy()
    pos_y1  = -1024
    pos_y2  = 0

    ship    = Ship(ai_settings, screen)
    bullets = Group()

    while True:
        # 按键事件
        gf.check_events(ai_settings, screen, ship, bullets)

        # 飞机/子弹 更新
        ship.update()
        gf.update_bullets(bullets)

        # 背景滚动
        screen.blit(bg_img1, (0, pos_y1))
        screen.blit(bg_img2, (0, pos_y2))

        pos_y1 += ai_settings.bg_roll_speed_factor
        pos_y2 += ai_settings.bg_roll_speed_factor

        if pos_y1 > 0:
            pos_y1 = -1024
        if pos_y2 > 1024:
            pos_y2 = 0

        gf.update_screen(ai_settings, screen, ship, bullets)

run_game()