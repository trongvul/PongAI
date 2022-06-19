class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.screen_caption = "Pong"
        self.bg_color = (0, 0, 0)
        self.object_color = (250, 250, 250)

        self.paddle_width = 15
        self.paddle_height = 80
        self.paddle_speed = 10
        self.paddle1_x = 10
        self.paddle1_y = self.screen_height // 2
        self.paddle2_x = self.screen_width - self.paddle_width - 10
        self.paddle2_y = self.screen_height // 2

        self.ball_width = 15
        self.ball_height = 15
        self.ball_speed = 8
