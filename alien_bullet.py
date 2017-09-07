import pygame
from pygame.sprite import Sprite

class Alien_bullet(Sprite):
    def __init__(self, ai_settings, screen, bullet_speed, ship):
        super().__init__()
        self.screen = screen

        self.image = pygame.transform.scale(pygame.image.load('images/alien_bullet.png').convert_alpha(), (15, 15))
        self.rect  = self.image.get_rect()
        # self.rect  = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        self.y = float(self.rect.y)
        self.speed_factor = bullet_speed



    def update(self):
        self.y += self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        self.screen.blit(self.image, self.rect)
        # pygame.draw.rect(self.screen, self.color, self.rect)

