import pygame
from random import randint
from pygame.sprite import Sprite

class Alien(Sprite):

    def __init__(self, ai_settings, screen):
        super().__init__()

        self.screen = screen
        self.ai_settings = ai_settings

        alien_num  = randint(1, 3)
        self.image = pygame.image.load('images/alien_' + str(alien_num) + '.png')
        self.rect  = self.image.get_rect()
        self.score = 10 # 击落本机获得的分数

        # 敌机移动速度
        self.alien_speed_factor = 2
        self.fleet_drop_speed   = randint(4, 8)

        # 1向右移动，-1向左移动
        self.fleet_direction = 1

        self.rect.x = randint(self.rect.width, ai_settings.screen_width - self.rect.width)
        self.rect.y = -self.rect.height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        # self.check_edges()
        # self.x += self.alien_speed_factor * self.fleet_direction
        # self.rect.x = self.x
        self.y += self.fleet_drop_speed
        self.rect.y = self.y

    def check_edges(self, type):
        screen_rect = self.screen.get_rect()

        if type == 'bottom' and self.rect.bottom >= screen_rect.bottom:
            return True

        return False
        # if self.rect.right >= screen_rect.right or self.rect.left <= 0:
        #     self.rect.y += self.fleet_drop_speed
        #     self.fleet_direction *= -1

