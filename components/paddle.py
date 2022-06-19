import pygame


class Paddle:
    def __init__(self, pong_game, x, y):
        self.screen = pong_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = pong_game.settings
        self.color = self.settings.object_color

        self.rect = pygame.Rect(
            x, y, self.settings.paddle_width, self.settings.paddle_height)

        self.y = float(self.rect.y)
        self.speed = self.settings.paddle_speed
        self.moving_up = False
        self.moving_down = False

    def reset(self):
        self.rect.centery = self.screen_rect.centery
        self.y = float(self.rect.y)
        self.speed = self.settings.paddle_speed
        self.moving_up = False
        self.moving_down = False

    def update(self):
        if self.moving_up and self.rect.top > 0:
            self.y -= self.speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.speed

        self.rect.y = self.y

    def draw_paddle(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
