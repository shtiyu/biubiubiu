class GameStats():
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.game_active = False
        self.high_score  = 0
        self.game_time = 0
        self.reset_stats()

    # 增加总游戏时间
    def increase_time(self, time_passed):
        self.game_time += time_passed

    # 获取总游戏时间
    def get_game_time(self):
        return self.game_time

    def reset_stats(self):
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.game_time = 0
        self.ai_settings.initialize_dynamic_setting()