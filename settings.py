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

        self.alien_num_min  = 3 # 每次最低出现敌机数

        self.alien_create_sec = 4000 # 每隔多少毫秒生成一次敌机


    def initialize_dynamic_setting(self):
        self.ship_speed_factor   = 5
        self.bullet_speed_factor = 20
        self.game_level = 1
        self.alien_num_min = 3  # 每次最低出现敌机数
        self.alien_create_sec = 4000  # 每隔多少毫秒生成一次敌机

    # 当时间减为小于0时，返回True,生成新敌机
    def decrease_time(self, time_passed):
        self.alien_create_sec -= time_passed
        if self.alien_create_sec < 0:
            self.alien_create_sec = 4000 - (int(self.game_level / 3) * 100)
            return True
        return False

    def level_up(self, total_game_time):
        # self.ship_speed_factor   *= self.speedup_scale
        # self.bullet_speed_factor *= self.speedup_scale

        # 7秒增加一级等级
        cal_lvl = int(total_game_time / 10000)


        if cal_lvl > self.game_level:
            self.game_level = cal_lvl
        else:
            return True

        # 每2级提升一次难度
        if self.game_level % 2 == 0:
            # 本机增加1速度
            if self.ship_speed_factor < 8:
                self.ship_speed_factor += 1

            if self.alien_num_min < 8:
                self.alien_num_min += 1

            if self.alien_create_sec > 3:
                self.alien_create_sec = 4000 - (int(self.game_level / 3) * 100)
