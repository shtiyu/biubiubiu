import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard():

    def __init__(self, ai_settings, screen, stats):

        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats       = stats

        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 36)

        self.prep_ships()
        self.prep_score()
        self.prep_high_score()

    def prep_ships(self):
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.image = pygame.transform.scale(ship.image, (25, 24))
            ship.rect.x = 10 + ship_number * 25
            ship.rect.y = self.screen.get_rect().height - 40
            self.ships.add(ship)

    def prep_score(self):
        score_str = "{:,}".format(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
        self.ships.draw(self.screen)

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.ships.draw(self.screen)

    def prep_high_score(self):
        high_score = self.stats.high_score
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top
