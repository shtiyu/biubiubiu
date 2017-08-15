import pygame

class Ship():

    def __init__(self, ai_settings, screen):
        self.screen = screen
        self.ai_settings = ai_settings

        #self.image = pygame.transform.scale(pygame.image.load('images/ship.png').convert_alpha(), (62, 50))
        self.direction   = 'stop'
        self.air         = None
        self.air_rect    = pygame.Rect(0, 0, 40, 72) # 喷射火焰位置
        self.image_big   = pygame.image.load('images/player.png')
        self.image       = self.image_big.subsurface(pygame.Rect(92, 182, 184 - 92, 272 - 182))
        self.rect        = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom  = self.screen_rect.bottom
        self.centerX = float(self.rect.centerx)
        self.centerY = float(self.rect.centery)

        self.moving_right = False
        self.moving_left  = False
        self.moving_down  = False
        self.moving_up    = False

    # 设置飞机的图片
    def set_image(self, type):
        self.direction = type
        self.image     = self.get_image(type)

        if type == 'up':
            self.set_air('set')
        else:
            self.set_air('remove')

    # 向上飞时，增加喷射火焰
    def set_air(self, type):
        if type == 'set':
            self.air = pygame.image.load('images/air.png').subsurface(pygame.Rect(89, 5, 128 - 89, 77 - 5))
        elif type == 'remove':
            self.air = None

    # 获取不同方向的飞机
    def get_image(self, type):

        if type == 'left':
            rect  = pygame.Rect(94, 277, 177 - 94, 371 - 277)
            image = self.image_big.subsurface(rect)
        elif type == 'right':
            rect  = pygame.Rect(0, 364, 82, 457 - 364)
            image = self.image_big.subsurface(rect)
        else:
            rect  = pygame.Rect(92, 182, 184 - 92, 272 - 182)
            image = self.image_big.subsurface(rect)

        return image

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.centerX += self.ai_settings.ship_speed_factor

        if self.moving_left and self.rect.left > 0:
            self.centerX -= self.ai_settings.ship_speed_factor

        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.centerY += self.ai_settings.ship_speed_factor

        if self.moving_up and self.rect.top > 0:
            self.centerY -= self.ai_settings.ship_speed_factor

        self.rect.centerx = self.centerX
        self.rect.centery = self.centerY
        self.air_rect.centerx = self.centerX
        self.air_rect.centery = self.centerY + int((self.rect.height + 72 ) / 2) - 10  # 飞机中心+(飞机高度+火焰高度)/2

    def blitme(self):
        self.screen.blit(self.image, self.rect)
        if self.air:
            self.screen.blit(self.air, self.air_rect)

    def center_ship(self):
        self.centerX = self.screen_rect.centerx
        self.centerY = self.screen_rect.height - self.rect.height
        self.set_image('stop')