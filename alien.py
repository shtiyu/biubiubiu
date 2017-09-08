import pygame
from random import randint
from pygame.sprite import Sprite
from alien_bullet import Alien_bullet

class Alien(Sprite):

    def __init__(self, ai_settings, screen, alien_bullets):
        super().__init__()

        self.screen = screen
        self.ai_settings = ai_settings
        self.bullets = alien_bullets

        alien_num  = randint(1, 3)
        self.image = pygame.image.load('images/alien_' + str(alien_num) + '.png')
        self.rect  = self.image.get_rect()
        self.score = 10 # 击落本机获得的分数

        self.fire_img = pygame.image.load('images/alien_bullet.png')

        # 敌机移动速度
        fleet_drop_speed        = randint(4, 12)
        self.alien_speed_factor = 2
        self.fleet_drop_speed   = fleet_drop_speed
        self.bullet_speed       = fleet_drop_speed + randint(4, 8) + ai_settings.game_level

        # 1向右移动，-1向左移动
        self.fleet_direction = 1

        self.passed_time = 0

        self.fire_gap = randint(500, 700) # 发射间隔

        self.rect.x = randint(self.rect.width, ai_settings.screen_width - self.rect.width)
        self.rect.y = -self.rect.height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.next_x = None

    # 敌机攻击
    def fire(self):
        a_bullet = Alien_bullet(self.ai_settings, self.screen, self.bullet_speed, self)
        self.bullets.add(a_bullet)

    def blitme(self, passed_time, stats):
        self.passed_time += passed_time
        gap = self.fire_gap - (self.ai_settings.game_level * 10)

        if gap < 300:
            gap = 300

        if self.passed_time > gap and self.rect.y > 0 and stats.game_active:
            self.fire()
            self.passed_time = 0
        self.screen.blit(self.image, self.rect)

    def update(self):
        # self.check_edges()
        # self.x += self.alien_speed_factor * self.fleet_direction
        # self.rect.x = self.x

        # 随机向左右移动
        if self.next_x == None:
            self.next_x = randint(0, self.screen.get_rect().width)
        else:
            if self.next_x > self.x:
                self.x += 1
            elif self.next_x < self.x:
                self.x -= 1
            else:
                self.next_x = None

        self.y += self.fleet_drop_speed
        self.rect.y = self.y
        self.rect.x = self.x

    def resetPos(self, x="", y=""):
        if x != "":
            self.rect.x = int(x)

        if y != "":
            self.rect.y = int(y)

    def check_edges(self, type):
        screen_rect = self.screen.get_rect()

        if type == 'bottom' and self.rect.bottom >= screen_rect.bottom:
            return True

        return False
        # if self.rect.right >= screen_rect.right or self.rect.left <= 0:
        #     self.rect.y += self.fleet_drop_speed
        #     self.fleet_direction *= -1

