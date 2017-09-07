class Settings():

    def __init__(self):
        self.screen_width  = 400
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 飞船速度
        self.ship_speed_factor = 5
        # 飞船生命数
        self.ship_limit = 3

        # 子弹
        self.bullet_speed_factor = 20
        self.bullets_allowed = 3

        # 背景滚动速度
        self.bg_roll_speed_factor = 2

        # 本机增速权重
        self.speedup_scale = 1.1

        # 敌机数量增加权重
        self.alien_scale = 1.1

        # 难度等级
        self.game_level = 1

        self.initialize_dynamic_setting()

    def initialize_dynamic_setting(self):
        self.ship_speed_factor   = 5
        self.bullet_speed_factor = 20
        self.game_level = 1

    def level_up(self):
        # self.ship_speed_factor   *= self.speedup_scale
        # self.bullet_speed_factor *= self.speedup_scale
        self.game_level += 1

        if self.game_level % 3 == 0:
            if self.bullets_allowed <= 3:
                self.bullets_allowed += 1

