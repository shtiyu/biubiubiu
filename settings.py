class Settings():

    def __init__(self):
        self.screen_width  = 400
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 飞船速度
        self.ship_speed_factor = 5
        # 飞船生命数
        self.ship_limit = 3

        #子弹
        self.bullet_speed_factor = 20
        self.bullets_allowed = 3

        #背景滚动速度
        self.bg_roll_speed_factor = 2
