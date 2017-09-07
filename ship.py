import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    _rate = 100 # 每帧需要停留的毫秒数

    def __init__(self, ai_settings, screen, size=1):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #self.image = pygame.transform.scale(pygame.image.load('images/ship.png').convert_alpha(), (62, 50))
        self.direction   = 'stop'
        self.image_big   = pygame.image.load('images/player.png').convert()
        self.image       = self.image_big.subsurface(pygame.Rect(92, 182, 184 - 92, 272 - 182))
        self.rect        = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx  = self.screen_rect.centerx
        self.rect.centery  = self.screen_rect.bottom - self.rect.height
        self.centerX = float(self.rect.centerx)
        self.centerY = float(self.rect.centery)

        self.air = None
        self.air_rect = pygame.Rect(self.centerX - 20,
                                    self.centerY + int((self.rect.height + 72) / 2) - 10 - 36,
                                    40, 72)  # 喷射火焰位置

        self.moving_right = False
        self.moving_left  = False
        self.moving_down  = False
        self.moving_up    = False

        self.alive_state  = True  # 活着的状态
        self.crash_frames = []    # 机毁人亡序列
        self.passed_time  = 0

        self.invincible_time = 0 #复活有3秒无敌时间

    def check_invincible(self):
        if self.invincible_time > 0:
            return True
        else:
            return False

    # 设置飞机的图片
    def set_image(self, type):
        self.direction = type
        self.image     = self.get_image(type)

        if self.moving_up:
            self.set_air('set')
        else:
            self.set_air('remove')

    # 向上飞时，增加喷射火焰
    def set_air(self, type):
        if type == 'set':

            air = pygame.image.load('images/air.png')

            if self.moving_left:
                img = air.subsurface(pygame.Rect(138, 2, 176 - 138, 78 - 2))
            elif self.moving_right:
                img = pygame.transform.flip(air.subsurface(pygame.Rect(138, 2, 176 - 138, 78 - 2)), True, False)
            else:
                img = air.subsurface(pygame.Rect(89, 5, 128 - 89, 77 - 5))

            self.air = img
        elif type == 'remove':
            self.air = None

    # 获取不同方向的飞机
    def get_image(self, type):

        if self.moving_left:
            rect = pygame.Rect(94, 277, 177 - 94, 371 - 277)
            image = self.image_big.subsurface(rect)
        elif self.moving_right:
            rect = pygame.Rect(94, 277, 177 - 94, 371 - 277)
            image = pygame.transform.flip(self.image_big.subsurface(rect), True, False)
        else:
            rect = pygame.Rect(92, 182, 184 - 92, 272 - 182)
            image = self.image_big.subsurface(rect)

        return image

    def update(self):

        # 尾焰偏移
        offset = 0

        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.centerX += self.ai_settings.ship_speed_factor
            if self.moving_up:
                offset = -2

        if self.moving_left and self.rect.left > 0:
            self.centerX -= self.ai_settings.ship_speed_factor
            if self.moving_up:
                offset = -2

        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.centerY += self.ai_settings.ship_speed_factor

        if self.moving_up and self.rect.top > 0:
            self.centerY -= self.ai_settings.ship_speed_factor

        self.rect.centerx = self.centerX
        self.rect.centery = self.centerY
        self.air_rect.centerx = self.centerX  + offset
        self.air_rect.centery = self.centerY + int((self.rect.height + 72 ) / 2) - 10  # 飞机中心+(飞机高度+火焰高度)/2

    def blitme(self, passed_time):

        alpha = self.image.get_alpha()
        if self.invincible_time > 0:
            self.image.set_alpha(self.invincible_time % 255)
            self.invincible_time -= passed_time
        elif alpha is None or  alpha < 255:
            self.image.set_alpha(255)

        if self.alive_state and self.image:
            self.screen.blit(self.image, self.rect)
            if self.air:
                self.screen.blit(self.air, self.air_rect)
        else:
            self.passed_time += passed_time
            self.order = int((self.passed_time / self._rate)) % 6
            self.image = self.crash_frames[self.order]
            self.screen.blit(self.image, self.crash_rect)

            if self.order == 5:
                self.set_image('stop')
                self.alive_state = True
                self.passed_time = 0
                self.center_ship()


    def center_ship(self):

        self.centerX  = self.screen_rect.centerx
        self.centerY  = self.screen_rect.bottom - self.rect.height
        self.set_image('stop')

    # 获取坠机图片序列
    def set_crash_image_frames(self):

        crash_image = pygame.image.load('images/player_crash_3.png')
        self.crash_frames = [crash_image.subsurface(
            pygame.Rect((i * 210), 0, 210, 208)
        ) for i in range(0, 6)]

    # 被击毁
    def crash(self):
        self.crash_rect        = pygame.Rect(0, 0, 210, 208)
        self.crash_rect.center = self.rect.center
        self.set_crash_image_frames()
        self.alive_state = False
        self.order = 0
        self.invincible_time = 3000





